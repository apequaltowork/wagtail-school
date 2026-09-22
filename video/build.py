"""
Video renderer for "I Upgraded Wagtail 2.7 -> 7.4".

Adapted from the Wagtail Unboxed series pipeline (github.com/apequaltowork/wagtail-unbox).

Pipeline, all local, no cloud services:

    scene spec (video/<key>/scenes.py)
        -> HTML slide  (theme.css)
        -> PNG 1920x1080  (headless Chrome)
        -> narration audio  (edge-tts neural voice, or Windows SAPI offline)
        -> per-scene MP4 segment  (ffmpeg, still + audio + fades)
        -> concatenated episode MP4 + SRT subtitles

Usage:
    python video/build.py upgrade                 # full render, neural narration
    python video/build.py upgrade --voice en-GB-RyanNeural
    python video/build.py upgrade --engine sapi   # offline fallback, robotic
    python video/build.py upgrade --silent        # no narration; fixed per-scene durations
    python video/build.py upgrade --stills-only   # just the PNGs, for checking the design
    python video/build.py upgrade --scene 3       # render one scene (fast iteration)

Output lands in video/<key>/out/.

Narration defaults to the neural voice en-US-SteffanNeural via edge-tts, which sends
the narration text to Microsoft to synthesise and so needs a network connection.
`--engine sapi` falls back to the offline Windows voices, which are robotic and are
only useful as a scratch track.

To record your own voice instead: render with --silent, read from
video/<key>/out/narration.txt (every line carries its timecode), and re-render.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

import cards

VIDEO_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(VIDEO_DIR))
REPO = VIDEO_DIR.parent
# Everything for a video lives in one folder: video/<key>/
EPISODE_ROOT = VIDEO_DIR
THEME = VIDEO_DIR / "theme.css"

WIDTH, HEIGHT, FPS = 1920, 1080, 30

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

# Padding around narration so scenes breathe.
LEAD_IN = 0.35
LEAD_OUT = 0.9
SILENT_DEFAULT = 4.0
FADE = 0.35


# --------------------------------------------------------------------------- spec


@dataclass
class Scene:
    """One slide + the sentence spoken over it."""

    id: str
    body: str                      # inner HTML of .slide
    say: str = ""                  # narration; "" = silent beat
    hold: float | None = None      # force a duration (seconds)
    classes: str = ""              # extra classes on .slide
    full_page: str = ""            # complete HTML doc; bypasses the .slide wrapper
    # Animated scene: one body-HTML string per frame, played at FPS and then
    # held on the last frame for whatever narration time remains. See term.py.
    frames: list[str] = field(default_factory=list)


@dataclass
class Episode:
    key: str
    title: str
    badge: str
    scenes: list[Scene] = field(default_factory=list)
    # Episode number as it appears on the intro card, e.g. "0a" or "07".
    # Defaults to whatever follows "ep" in `key`.
    number: str | None = None
    # Spoken over the intro / end cards. "" leaves them silent.
    intro_say: str = ""
    outro_say: str = ""
    intro_hold: float = 4.0
    # 10s on the end card: YouTube end-screen widgets need a 5s minimum and will
    # cover whatever they sit on, so this leaves ~5s of the card readable first.
    outro_hold: float = 10.0

    @property
    def ep_number(self) -> str:
        return self.number or self.key.removeprefix("ep")


# --------------------------------------------------------------------------- utils


def run(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def find_chrome() -> Path:
    for p in CHROME_CANDIDATES:
        if p.exists():
            return p
    sys.exit("No Chrome or Edge found -- needed to rasterise slides.")


def need(tool: str) -> str:
    path = shutil.which(tool)
    if not path:
        sys.exit(f"{tool} not found on PATH.")
    return path


def probe_duration(path: Path) -> float:
    out = run([need("ffprobe"), "-v", "error", "-show_entries", "format=duration",
               "-of", "csv=p=0", str(path)]).stdout.strip()
    return float(out)


def timecode(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


# --------------------------------------------------------------------------- render


def write_html(scene: Scene, ep: Episode, dest: Path) -> Path:
    if scene.full_page:
        dest.write_text(scene.full_page, encoding="utf-8")
        return dest
    html = f"""<!doctype html>
<html><head><meta charset="utf-8">
<link rel="stylesheet" href="{THEME.as_uri()}">
</head><body>
<div class="slide {scene.classes}">
{scene.body}
<div class="badge">{ep.badge}</div>
</div>
</body></html>"""
    dest.write_text(html, encoding="utf-8")
    return dest


def shoot(chrome: Path, html: Path, png: Path) -> None:
    subprocess.run(
        [str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1",
         f"--window-size={WIDTH},{HEIGHT}",
         f"--screenshot={png}", str(html)],
        check=True, capture_output=True, text=True,
    )
    if not png.exists():
        raise RuntimeError(f"Chrome produced no screenshot for {html.name}")


def narrate_edge(lines: list[tuple[str, str]], out_dir: Path, voice: str, rate: str) -> None:
    """Neural narration via edge-tts (Microsoft Edge Read Aloud voices).

    Sends the narration text to Microsoft to synthesise, so it needs a network
    connection. Produces .mp3, which ffmpeg reads directly.
    """
    import asyncio

    import edge_tts

    async def one(stem: str, text: str) -> None:
        comm = edge_tts.Communicate(text, voice, rate=rate)
        await comm.save(str(out_dir / f"{stem}.mp3"))

    async def all_of_them() -> None:
        # A little concurrency, but not enough to get rate-limited.
        sem = asyncio.Semaphore(4)

        async def guarded(stem: str, text: str) -> None:
            async with sem:
                for attempt in range(3):
                    try:
                        await one(stem, text)
                        return
                    except Exception:
                        if attempt == 2:
                            raise
                        await asyncio.sleep(1.5 * (attempt + 1))

        await asyncio.gather(*(guarded(s, t) for s, t in lines))

    asyncio.run(all_of_them())


def narrate_sapi(lines: list[tuple[str, str]], out_dir: Path, voice: str) -> None:
    """Offline fallback: Windows SAPI. Robotic -- scratch track only."""
    if not lines:
        return
    spec = out_dir / "_narration.json"
    spec.write_text(json.dumps([{"id": i, "text": t} for i, t in lines]), encoding="utf-8")

    ps = f"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$items = Get-Content -Raw -LiteralPath '{spec}' | ConvertFrom-Json
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
$synth.SelectVoice('{voice}')
$synth.Rate = -1
foreach ($item in $items) {{
    $target = Join-Path '{out_dir}' ($item.id + '.wav')
    $synth.SetOutputToWaveFile($target)
    $synth.Speak($item.text)
}}
$synth.Dispose()
"""
    subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", ps],
                   check=True, capture_output=True, text=True)


def make_animated_video(frames: list[Path], seconds: float, dest: Path) -> Path:
    """Play the frames at FPS, then hold the last one for the rest of the scene."""
    per = 1.0 / FPS
    played = len(frames) * per
    tail = max(seconds - played, 0.0)

    listing = dest.with_suffix(".concat.txt")
    lines = []
    for f in frames:
        lines.append(f"file '{f.as_posix()}'\nduration {per:.5f}\n")
    # Hold the last frame by repeating it one frame at a time rather than with a
    # single long `duration`. ffmpeg 9's concat demuxer silently drops that long
    # entry when it names the same file as the one before it, which leaves the
    # rest of the scene black -- the animation plays and then the picture dies
    # while the narration keeps going.
    for _ in range(int(round(tail * FPS))):
        lines.append(f"file '{frames[-1].as_posix()}'\nduration {per:.5f}\n")
    # The concat demuxer ignores the final entry's duration, so repeat it.
    lines.append(f"file '{frames[-1].as_posix()}'\n")
    listing.write_text("".join(lines), encoding="utf-8")

    silent = dest.with_suffix(".silent.mp4")
    run([need("ffmpeg"), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         # Plain -r gives constant frame rate, which is what we want: the concat
         # durations are already 1/FPS. (ffmpeg 9 rejects -r together with
         # -fps_mode vfr, and -vsync no longer exists.)
         "-i", str(listing), "-r", str(FPS),
         "-c:v", "libx264", "-preset", "medium", "-crf", "18",
         "-pix_fmt", "yuv420p", "-t", f"{seconds:.3f}", str(silent)])
    return silent


def make_segment(png: Path, wav: Path | None, seconds: float, dest: Path,
                 frames: list[Path] | None = None) -> None:
    ffmpeg = need("ffmpeg")
    fade_out_at = max(seconds - FADE, 0.01)
    vf = f"fade=t=in:st=0:d={FADE},fade=t=out:st={fade_out_at:.3f}:d={FADE},format=yuv420p"

    if frames:
        source = make_animated_video(frames, seconds, dest)
        cmd = [ffmpeg, "-y", "-loglevel", "error", "-i", str(source)]
    else:
        cmd = [ffmpeg, "-y", "-loglevel", "error",
               "-loop", "1", "-framerate", str(FPS), "-t", f"{seconds:.3f}", "-i", str(png)]
    if wav:
        # Pad the audio so narration sits inside the scene with lead-in/out.
        cmd += ["-i", str(wav),
                "-filter_complex",
                f"[1:a]adelay={int(LEAD_IN*1000)}|{int(LEAD_IN*1000)},"
                f"apad=whole_dur={seconds:.3f}[a]",
                "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    else:
        cmd += ["-f", "lavfi", "-t", f"{seconds:.3f}", "-i", "anullsrc=r=48000:cl=stereo",
                "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k"]

    cmd += ["-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-r", str(FPS), "-t", f"{seconds:.3f}", str(dest)]
    run(cmd)


def build(ep: Episode, silent: bool, stills_only: bool, only: int | None,
          voice: str, engine: str, rate: str) -> None:
    out = EPISODE_ROOT / ep.key / "out"
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    chrome = find_chrome()

    if only is None:
        # Every episode opens on the branded intro card and closes on the end
        # card, so they can never drift from brand.py or be forgotten in the edit.
        scenes = [
            Scene(id="intro_card", body="", say=ep.intro_say, hold=ep.intro_hold,
                  full_page=cards.intro_html(ep.key)),
            *ep.scenes,
            Scene(id="end_card", body="", say=ep.outro_say, hold=ep.outro_hold,
                  full_page=cards.end_html(ep.key)),
        ]
    else:
        scenes = [ep.scenes[only]]

    print(f"\n{ep.title}\n{'=' * len(ep.title)}")
    print(f"{len(scenes)} scene(s) -> {out}\n")

    # 1. slides (a scene is either one still, or a frame sequence)
    pngs: list[Path] = []
    seqs: list[list[Path] | None] = []
    for i, sc in enumerate(scenes):
        stem = f"{i:03d}_{sc.id}"
        if sc.frames:
            frame_dir = work / stem
            frame_dir.mkdir(exist_ok=True)
            shots: list[Path] = []
            for n, body in enumerate(sc.frames):
                frame = Scene(id=sc.id, body=body, classes=sc.classes)
                html = write_html(frame, ep, frame_dir / f"f{n:05d}.html")
                png = frame_dir / f"f{n:05d}.png"
                shoot(chrome, html, png)
                shots.append(png)
            seqs.append(shots)
            pngs.append(shots[-1])
            print(f"  anim   {stem}  ({len(shots)} frames)")
        else:
            html = write_html(sc, ep, work / f"{stem}.html")
            png = work / f"{stem}.png"
            shoot(chrome, html, png)
            seqs.append(None)
            pngs.append(png)
            print(f"  slide  {stem}.png")

    if stills_only:
        print(f"\nStills only. Open {work} to review the design.")
        return

    # 2. narration
    durations: list[float] = []
    wavs: list[Path | None] = []
    if silent:
        for sc in scenes:
            floor = len(sc.frames) / FPS if sc.frames else 0.0
            durations.append(max(sc.hold or SILENT_DEFAULT, floor))
            wavs.append(None)
    else:
        todo = [(f"{i:03d}_{sc.id}", sc.say) for i, sc in enumerate(scenes) if sc.say.strip()]
        print(f"\n  narrating {len(todo)} line(s) with '{voice}' ({engine}) ...")
        if engine == "edge":
            narrate_edge(todo, work, voice, rate)
        else:
            narrate_sapi(todo, work, voice)
        for i, sc in enumerate(scenes):
            stem = f"{i:03d}_{sc.id}"
            wav = work / f"{stem}.mp3"
            if not wav.exists():
                wav = work / f"{stem}.wav"
            floor = len(sc.frames) / FPS if sc.frames else 0.0
            if sc.say.strip() and wav.exists():
                spoken = probe_duration(wav)
                durations.append(max(sc.hold or (spoken + LEAD_IN + LEAD_OUT), floor))
                wavs.append(wav)
            else:
                durations.append(max(sc.hold or SILENT_DEFAULT, floor))
                wavs.append(None)

    # 3. segments
    segs: list[Path] = []
    for i, (png, wav, secs) in enumerate(zip(pngs, wavs, durations)):
        seg = work / f"seg_{i:03d}.mp4"
        make_segment(png, wav, secs, seg, frames=seqs[i])
        segs.append(seg)
        print(f"  segment {i:03d}  {secs:6.2f}s")

    # 4. concat
    listing = work / "concat.txt"
    listing.write_text("".join(f"file '{p.as_posix()}'\n" for p in segs), encoding="utf-8")
    final = out / f"{ep.key}.mp4"
    # Normalise loudness to about -16 LUFS, which is where YouTube wants spoken content.
    run([need("ffmpeg"), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0",
         "-i", str(listing), "-c:v", "copy",
         "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", str(final)])

    # 5. subtitles + narration script with real timecodes
    srt, script, clock = [], [], 0.0
    for i, (sc, secs) in enumerate(zip(scenes, durations), start=1):
        if sc.say.strip():
            start, end = clock + LEAD_IN, clock + secs - LEAD_OUT * 0.5
            srt.append(f"{i}\n{timecode(start)} --> {timecode(end)}\n{sc.say}\n")
            script.append(f"[{timecode(clock)[:-4]}] {sc.id}\n    {sc.say}\n")
        clock += secs
    (out / f"{ep.key}.srt").write_text("\n".join(srt), encoding="utf-8")
    (out / "narration.txt").write_text(
        f"{ep.title}\nTotal: {clock/60:.1f} min\n\n" + "\n".join(script), encoding="utf-8")

    total = probe_duration(final)
    print(f"\n  DONE  {final}")
    print(f"        {total/60:.2f} min  ({total:.1f}s)  {WIDTH}x{HEIGHT} @ {FPS}fps")
    print(f"        subtitles: {ep.key}.srt")
    print(f"        narration script: narration.txt\n")


# --------------------------------------------------------------------------- cli


def load_episode(key: str) -> Episode:
    """Load video/<key>/scenes.py as the video spec."""
    spec_path = EPISODE_ROOT / key / "scenes.py"
    if not spec_path.exists():
        sys.exit(f"No scene spec at {spec_path.relative_to(REPO)}")
    import importlib.util

    spec = importlib.util.spec_from_file_location(f"scenes_{key}", spec_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EPISODE


def main() -> None:
    ap = argparse.ArgumentParser(description="Render the upgrade video.")
    ap.add_argument("episode", help="video key, e.g. upgrade")
    ap.add_argument("--silent", action="store_true", help="no narration")
    ap.add_argument("--stills-only", action="store_true", help="render PNGs only")
    ap.add_argument("--scene", type=int, default=None, help="render a single scene by index")
    ap.add_argument("--engine", choices=["edge", "sapi"], default="edge",
                    help="edge = neural (needs internet); sapi = offline, robotic")
    ap.add_argument("--voice", default=None,
                    help="default: en-US-SteffanNeural (edge) / Microsoft Zira Desktop (sapi)")
    ap.add_argument("--rate", default="-4%", help="edge speaking rate, e.g. -8%% or +5%%")
    args = ap.parse_args()

    voice = args.voice or ("en-US-SteffanNeural" if args.engine == "edge"
                           else "Microsoft Zira Desktop")
    build(load_episode(args.episode), args.silent, args.stills_only, args.scene,
          voice, args.engine, args.rate)


if __name__ == "__main__":
    main()
