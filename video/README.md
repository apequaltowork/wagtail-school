# Video: "I Upgraded Wagtail 2.7 → 7.4 — Everything That Broke"

This folder builds the video that goes with [`blog/`](../blog/). The pipeline is adapted from the
Wagtail Unboxed series ([github.com/apequaltowork/wagtail-unbox](https://github.com/apequaltowork/wagtail-unbox)).

```
video/
  build.py          scene spec -> slides (headless Chrome) -> narration (edge-tts) -> MP4 + SRT
  term.py           animated terminal scenes (commands type out, real output appears)
  cards.py          intro card, end card, thumbnail
  theme.css         slide theme
  upgrade/
    scenes.py       the script: 42 scenes, following the blog post
    assets/         intro.png, end.png, thumb.png (1280x720 YouTube thumbnail)
    out/            upgrade.srt, narration.txt (with timecodes); the MP4 is not committed
    youtube.md      title, description, chapters and tags for upload
```

## Render

Needs Chrome or Edge, ffmpeg/ffprobe on PATH, and a Python with `edge-tts` installed.

```bash
python video/cards.py                               # cards and thumbnail
python video/build.py upgrade --stills-only         # check the slides
python video/build.py upgrade                       # full render, neural narration
python video/build.py upgrade --scene 12            # re-render one scene
```

Narration uses the neural voice `en-US-SteffanNeural` through edge-tts, which sends the narration
text to Microsoft to synthesise. To record your own voice: render with `--silent`, read from
`upgrade/out/narration.txt` (every line has its timecode), and re-render.

Every terminal output in `scenes.py` is pasted from `notes/logs/`. The log numbers are in the comments.
