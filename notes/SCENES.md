# Scenes

Moments worth showing on camera.
Format: `[SCENE] <title> — log NNN / commit <sha> / screenshot <file> — why it matters`

[SCENE] "Missing expected target directory" — log 002 — uv's Python 3.8 install half-fails on Windows. Installing a 2019 Python in 2026 is its own small adventure.
[SCENE] makemigrations won't run without a database — log 007 — Django 2.2 checks migration history against the live DB (it only became a warning in Django 3.1). An early taste of how old the stack is.
[SCENE] "Te reo Māori" crashes the seed — log 012 — Django's console email backend on Windows writes cp1252 to a pipe, so one macron in a fictional parent's answer kills the run. A reminder that the accented form data is deliberate, and it's already paying off.
[SCENE] The form keys we're about to break — baseline/form_field_keys.json / log 023 — Wagtail 2.7 stores "Parent/Guardian's full name" as `parentguardians-full-name` and "Languages spoken at home (e.g. Français, Español)" as `languages-spoken-at-home-eg-francais-espanol`. Show this file now; it's the "before" of the 2.10 clean_name change.
[SCENE] `from collections import Mapping` — log 028 — `python -Wa manage.py check` on 2.7 warns that Wagtail's own rich-text code "will stop working" in Python 3.10. It's the reason the 2.15 hop can't just bump Python.
[SCENE] Search 500 caught by the crawler — commit 6189150 — `{{ title|default:page.title }}` blows up in a non-page view. The baseline crawler earned its keep before the upgrade even started.
[SCENE] The admin in 2019 — screenshots/2.7/a05-edit-event-page.png, a13-submissions-enquiry.png — the teal 2.x editor with StreamFieldPanel, SnippetChooserPanel and the old form-data listing. Pair these with the 7.4 versions.
[SCENE] Stretched cards — commit 66d9b15 — the rendition's width/height attributes versus Bootstrap 4's card-img-top. A small real-world CSS bug, fixed before the baseline was recorded.
