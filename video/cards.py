"""Intro card, end card and thumbnail for the upgrade video.

    python video/cards.py          # writes video/upgrade/assets/{intro,end,thumb}.png

Same design language as the Wagtail Unboxed series cards (same channel), adapted for a
standalone video. build.py burns the intro and end cards into the MP4 itself.

The end card leaves the RIGHT THIRD clear: YouTube overlays its end-screen elements there.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
THEME = HERE / "theme.css"
ASSETS = HERE / "upgrade" / "assets"
WIDTH, HEIGHT = 1920, 1080

CHROME_CANDIDATES = [
    Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"),
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
]

BRAND = {
    "channel": "@apequaltowork",
    "repo": "github.com/apequaltowork/wagtail-school",
    "blog": "blog/ in the repo",
    "website": "apequaltowork.github.io/ashish-pitroda",
    "email": "apequaltowork@gmail.com",
    "youtube": "@apequaltowork",
    "linkedin": "in/ashish-pitroda",
    "stack": "Wagtail 2.7 &rarr; 2.15 &rarr; 7.4 &nbsp;&middot;&nbsp; Django 2.2 &rarr; 5.2 &nbsp;&middot;&nbsp; Python 3.8 &rarr; 3.12",
}

CARD_CSS = """
.todo { color: var(--amber); font-weight: 700; letter-spacing: 1px; }

/* ---------- shared mark: an opened box ---------- */
.mark { width: 104px; height: 104px; display: block; }

/* ---------- intro card ---------- */
.intro {
  width: 1920px; height: 1080px; position: relative;
  background:
    radial-gradient(1200px 700px at 78% 18%, rgba(67,177,176,.16), transparent 60%),
    linear-gradient(160deg, #0f1117 0%, #141826 58%, #0f1117 100%);
  display: flex; flex-direction: column; justify-content: center;
  padding: 0 140px; overflow: hidden;
}
/* faint grid, so the flat background has some texture */
.intro::after {
  content: ""; position: absolute; inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,.028) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,.028) 1px, transparent 1px);
  background-size: 80px 80px;
  mask-image: radial-gradient(900px 620px at 72% 30%, #000 0%, transparent 78%);
}
.intro > * { position: relative; z-index: 2; }

.brandline { display: flex; align-items: center; gap: 30px; margin-bottom: 76px; }
.brandline .word { font-size: 40px; letter-spacing: 9px; text-transform: uppercase; font-weight: 600; }
.brandline .word b { color: var(--teal); }
.brandline .tag {
  font-size: 26px; color: var(--muted); letter-spacing: 3px;
  text-transform: uppercase; padding-left: 30px; border-left: 3px solid var(--line);
}

.epline { display: flex; align-items: flex-start; gap: 56px; }
.epnum {
  font-size: 220px; font-weight: 800; line-height: .82; letter-spacing: -8px;
  color: transparent; -webkit-text-stroke: 4px var(--teal); flex: none;
}
.epwrap { padding-top: 14px; }
.epwrap .kicker {
  font-size: 30px; letter-spacing: 7px; text-transform: uppercase;
  color: var(--teal); margin-bottom: 26px; font-weight: 600;
}
.eptitle { font-size: 92px; font-weight: 700; line-height: 1.06; letter-spacing: -2.5px; max-width: 1260px; }

.stack {
  position: absolute; left: 140px; bottom: 92px; z-index: 2;
  font-family: var(--mono); font-size: 27px; color: var(--muted);
}
.intro .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); z-index: 3; }
.repoline {
  position: absolute; right: 140px; bottom: 92px; z-index: 2;
  font-family: var(--mono); font-size: 27px; color: var(--muted);
}

/* ---------- end card ---------- */
.end {
  width: 1920px; height: 1080px; position: relative;
  background:
    radial-gradient(900px 640px at 22% 76%, rgba(67,177,176,.15), transparent 62%),
    linear-gradient(200deg, #0f1117 0%, #141826 60%, #0f1117 100%);
  padding: 110px 140px; overflow: hidden;
  display: flex; flex-direction: column; justify-content: space-between;
}
.end .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 14px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); }
/* YouTube drops its clickable end-screen widgets over the right third. */
.safe {
  position: absolute; right: 0; top: 0; width: 620px; height: 1080px;
  border-left: 2px dashed rgba(255,255,255,.07);
}
.safe .note {
  position: absolute; top: 50%; left: 50%; transform: translate(-50%,-50%) rotate(-90deg);
  white-space: nowrap; font-size: 22px; letter-spacing: 6px; text-transform: uppercase;
  color: rgba(255,255,255,.13);
}
.end .inner { max-width: 1120px; position: relative; z-index: 2; }
.end h1 { font-size: 88px; line-height: 1.05; letter-spacing: -2px; margin: 0 0 22px; }
.end .sub2 { font-size: 36px; color: var(--muted); margin-bottom: 64px; }

.links { display: flex; flex-direction: column; gap: 30px; }
.link { display: flex; align-items: center; gap: 26px; }
.link .lbl {
  font-size: 22px; letter-spacing: 3px; text-transform: uppercase; color: var(--teal);
  width: 180px; flex: none; font-weight: 600;
}
/* 32px keeps the longest value (the repo URL) on one line inside .inner. */
.link .val { font-family: var(--mono); font-size: 32px; color: var(--fg); white-space: nowrap; }

.endfoot {
  position: relative; z-index: 2; display: flex; align-items: center;
  gap: 30px; color: var(--muted); font-size: 28px;
}
.endfoot .word { font-size: 30px; letter-spacing: 7px; text-transform: uppercase; color: var(--fg); }
.endfoot .word b { color: var(--teal); }
"""

MARK = """
<svg class="mark" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 22 L32 10 L58 22 L32 34 Z" stroke="#43b1b0" stroke-width="3"
        stroke-linejoin="round" fill="rgba(67,177,176,.16)"/>
  <path d="M6 22 V45 L32 57 V34" stroke="#43b1b0" stroke-width="3" stroke-linejoin="round"/>
  <path d="M58 22 V45 L32 57" stroke="#2b6f6e" stroke-width="3" stroke-linejoin="round"/>
  <path d="M32 30 V4 M32 4 L25 11 M32 4 L39 11" stroke="#eef1f7" stroke-width="3"
        stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""


THUMB_CSS = """
/* 1280x720 thumbnail: same design language, but sized to survive being shown
   at roughly 360x200 in a sidebar. Everything gets bigger, not smaller. */
.thumb {
  width: 1280px; height: 720px; position: relative; overflow: hidden;
  background:
    radial-gradient(760px 460px at 80% 20%, rgba(67,177,176,.20), transparent 62%),
    linear-gradient(160deg, #0f1117 0%, #141826 58%, #0f1117 100%);
  padding: 74px 84px; display: flex; flex-direction: column; justify-content: center;
}
.thumb .accent { position: absolute; left: 0; top: 0; bottom: 0; width: 12px;
  background: linear-gradient(180deg, var(--teal), var(--teal-dim)); }
.thumb .epbig {
  position: absolute; right: 60px; top: 40px;
  font-size: 210px; font-weight: 800; letter-spacing: -8px; line-height: 1;
  color: transparent; -webkit-text-stroke: 4px rgba(67,177,176,.42);
}
.thumb .word {
  font-size: 30px; letter-spacing: 8px; text-transform: uppercase;
  font-weight: 600; margin-bottom: 30px;
}
.thumb .word b { color: var(--teal); }
.thumb h1 {
  font-size: 88px; font-weight: 800; line-height: 1.02; letter-spacing: -2.5px;
  margin: 0; max-width: 900px;
}
.thumb .hook {
  margin-top: 30px; font-size: 34px; color: var(--teal); font-weight: 600;
  letter-spacing: 1px;
}
"""


EXTRA_CSS = """
.big-arrow { color: var(--teal); }
.eptitle .ver { color: var(--teal); }
.thumb .vers { font-size: 118px; font-weight: 800; letter-spacing: -4px; line-height: 1; margin-bottom: 18px; }
.thumb .vers .arrow { color: var(--teal); }
.thumb .count { position: absolute; right: 70px; bottom: 60px; text-align: right; }
.thumb .count .n { font-size: 170px; font-weight: 800; line-height: .9; color: var(--red); letter-spacing: -6px; }
.thumb .count .l { font-size: 30px; letter-spacing: 6px; text-transform: uppercase; color: var(--muted); }
"""


def find_chrome() -> Path:
    for p in CHROME_CANDIDATES:
        if p.exists():
            return p
    sys.exit("No Chrome or Edge found -- needed to rasterise cards.")


def page(body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">
<link rel="stylesheet" href="{THEME.as_uri()}">
<style>{CARD_CSS}{THUMB_CSS}{EXTRA_CSS}</style></head><body>{body}</body></html>"""


def intro_html() -> str:
    return page(f"""
<div class="intro">
  <div class="accent"></div>
  <div class="brandline">
    {MARK}
    <div class="word">Wagtail <b>Upgrade</b></div>
    <div class="tag">Seven years in one video</div>
  </div>
  <div class="epwrap">
    <div class="kicker">Everything that broke</div>
    <div class="eptitle">I Upgraded Wagtail <span class="ver">2.7</span> &rarr; <span class="ver">7.4</span></div>
  </div>
  <div class="stack">{BRAND['stack']}</div>
  <div class="repoline">{BRAND['repo']}</div>
</div>""")


def end_html() -> str:
    rows = [("Code", BRAND["repo"]), ("Blog", BRAND["blog"]), ("Website", BRAND["website"]),
            ("YouTube", BRAND["youtube"]), ("LinkedIn", BRAND["linkedin"])]
    links = "\n".join(
        f'<div class="link"><div class="lbl">{lbl}</div><div class="val">{val}</div></div>'
        for lbl, val in rows)
    return page(f"""
<div class="end">
  <div class="accent"></div>
  <div class="safe"><div class="note">YouTube end-screen zone &mdash; keep clear</div></div>
  <div class="inner">
    <h1>Thanks for watching.</h1>
    <div class="sub2">Every step is a commit. Tags: v2.7-baseline &middot; v2.15 &middot; v7.4</div>
    <div class="links">{links}</div>
  </div>
  <div class="endfoot">
    {MARK}
    <div class="word">Wagtail <b>Upgrade</b></div>
    <div>&middot;</div>
    <div>{BRAND['channel']}</div>
  </div>
</div>""")


def thumb_html() -> str:
    return page("""
<div class="thumb">
  <div class="accent"></div>
  <div class="word">Wagtail <b>Upgrade</b></div>
  <div class="vers">2.7 <span class="arrow">&rarr;</span> 7.4</div>
  <h1 style="font-size:70px">Everything<br>that broke.</h1>
  <div class="count"><div class="n">22</div><div class="l">breakages</div></div>
</div>""")


def shoot(chrome: Path, html: str, dest: Path, size: tuple[int, int] = (WIDTH, HEIGHT)) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / f"_{dest.stem}.html"
    tmp.write_text(html, encoding="utf-8")
    subprocess.run(
        [str(chrome), "--headless", "--disable-gpu", "--hide-scrollbars",
         "--force-device-scale-factor=1", f"--window-size={size[0]},{size[1]}",
         f"--screenshot={dest}", str(tmp)],
        check=True, capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    print(f"  {dest}")


def main() -> None:
    chrome = find_chrome()
    shoot(chrome, intro_html(), ASSETS / "intro.png")
    shoot(chrome, end_html(), ASSETS / "end.png")
    shoot(chrome, thumb_html(), ASSETS / "thumb.png", size=(1280, 720))


if __name__ == "__main__":
    main()
