"""Animated terminal scenes.

A terminal on screen has to *move*, or it reads as a screenshot of a terminal.
This builds a frame sequence showing commands typing out character by character,
then their real captured output appearing.

    from term import Cmd, terminal_scene

    terminal_scene(
        scene_id="install",
        title="Installing Wagtail",
        bar="Windows . PowerShell",
        steps=[
            Cmd(text='pip install "wagtail==7.4.3"',
                out="Successfully installed wagtail-7.4.3 Django-6.1.1 ..."),
        ],
        say="...",
    )

Output is real: paste what the command actually printed. Inventing terminal
output in a teaching video is how viewers end up chasing a result that never
happens on their machine.
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field

from build import FPS, Scene

# Typing speed. 3 chars per frame at 30fps is ~90 c/s -- faster than real typing,
# but a video of realistic typing is unwatchable.
CHARS_PER_FRAME = 3
# Frames to hold after a command finishes typing, before its output appears.
PAUSE_AFTER_TYPE = 4
# Frames to hold on each chunk of output.
PAUSE_AFTER_OUT = 8


@dataclass
class Cmd:
    """One command: typed, then its output."""

    text: str
    out: str = ""
    prompt: str = "PS&gt;"
    # Output lines matching any of these render in teal rather than grey --
    # for the one line in the output that the narration is pointing at.
    highlight: list[str] = field(default_factory=list)
    # Output lines matching any of these render red -- for tracebacks and
    # failures, where teal would read as "this went well".
    error: list[str] = field(default_factory=list)


def _out_html(out: str, highlight: list[str], error: list[str] = ()) -> str:
    lines = []
    for raw in out.split("\n"):
        esc = html.escape(raw)
        if any(e in raw for e in error):
            cls = "err-out"
        elif any(h in raw for h in highlight):
            cls = "hl-out"
        else:
            cls = "o"
        lines.append(f'<span class="{cls}">{esc}</span>')
    return "\n".join(lines)


def _screen(bar: str, history: str, current: str) -> str:
    """history = already-completed lines; current = the line being typed."""
    body = history
    if current is not None:
        body += current
    return f"""
<div class="term term-big">
  <div class="bar">{bar}</div>
  <div class="body">{body}</div>
</div>"""


def terminal_frames(bar: str, steps: list[Cmd]) -> list[str]:
    """Every frame of the animation, as inner-HTML strings."""
    frames: list[str] = []
    history = ""

    for cmd in steps:
        raw = cmd.text
        typed = html.escape(raw)
        line_prefix = f'<span class="p">{cmd.prompt}</span> '

        # Type the command out. Slice the RAW text and escape afterwards --
        # slicing escaped text cuts entities like &quot; in half.
        for i in range(0, len(raw) + 1, CHARS_PER_FRAME):
            partial = html.escape(raw[:i])
            frames.append(_screen(bar, history, f'{line_prefix}{partial}<span class="cur">&nbsp;</span>'))
        # Whole command, cursor still blinking at the end.
        full_line = f'{line_prefix}{typed}<span class="cur">&nbsp;</span>'
        frames.extend([_screen(bar, history, full_line)] * PAUSE_AFTER_TYPE)

        history += f"{line_prefix}{typed}\n"

        if cmd.out:
            history += _out_html(cmd.out, cmd.highlight, cmd.error) + "\n"
            frames.extend([_screen(bar, history, "")] * PAUSE_AFTER_OUT)
        history += "\n"

    # Rest on the finished screen.
    frames.extend([_screen(bar, history, "")] * FPS)
    return frames


def terminal_scene(scene_id: str, title: str, bar: str, steps: list[Cmd],
                   say: str = "", eyebrow: str = "") -> Scene:
    """A Scene whose frames animate a terminal session."""
    head = ""
    if eyebrow:
        head += f'<div class="eyebrow">{eyebrow}</div>'
    if title:
        head += f"<h2 style=\"font-size:56px;margin-bottom:34px\">{title}</h2>"

    frames = [head + f for f in terminal_frames(bar, steps)]
    return Scene(id=scene_id, body=frames[-1], say=say, frames=frames)
