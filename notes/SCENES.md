# Scenes

Moments worth showing on camera.
Format: `[SCENE] <title> — log NNN / commit <sha> / screenshot <file> — why it matters`

[SCENE] "Missing expected target directory" — log 002 — uv's Python 3.8 install half-fails on Windows. Installing a 2019 Python in 2026 is its own small adventure.
[SCENE] makemigrations won't run without a database — log 007 — Django 2.2 checks migration history against the live DB (it only became a warning in Django 3.1). An early taste of how old the stack is.
[SCENE] "Te reo Māori" crashes the seed — log 012 — Django's console email backend on Windows writes cp1252 to a pipe, so one macron in a fictional parent's answer kills the run. A reminder that the accented form data is deliberate, and it's already paying off.
