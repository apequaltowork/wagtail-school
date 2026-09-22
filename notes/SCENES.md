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

## 2.7 → 2.15 hop
[SCENE] psycopg2 wants a C compiler — log 036 — the first thing that breaks is the Postgres driver, not Wagtail: there's no Python 3.10 wheel for psycopg2-binary 2.8. (B01)
[SCENE] "System check identified no issues", then every page crashes — logs 040 → 045 — `ModuleNotFoundError: No module named 'wagtail.core.middleware'` only shows on the first request. (B03)
[SCENE] **THE clean_name MOMENT** — logs 044, 048, 049, 053, 055 — after migrate, all 14 clean_names are blank. The 10-field enrolment form renders as ONE field named "". The admin CSV has ten columns all called "Subscribe to our newsletter", every value None. Running `check` to repair it crashes: "requires the unidecode library". One `pip install Unidecode` + `check` later: "Added `clean_name` on 10 form field(s)", and all 30 enquiries are back. Show it as before / broken / fixed. (B04)
[SCENE] New fields get new names — log 055 — "Parent/Guardian's full name" is stored as `parentguardians-full-name`, but a new field with the same label would get `parentguardians_full_name`. Two naming schemes in one form, forever.
[SCENE] The CSV button that isn't — log 048 — `?action=CSV` quietly returns the HTML page on 2.15; it's `?export=csv` now. (B05)
[SCENE] Byte-for-byte identical — log 072 — after six breakages, the crawler compares 2.15 with 2.7: same statuses, same page text, same counts, same CSV exports. The "it all came back" shot.
[SCENE] Same front end, new admin — screenshots/2.15 vs 2.7 — 12 front-end pages pixel-identical, while the editor gains History, Reports, comments and the new StreamField UI (a05-edit-event-page.png side by side).

## 2.15 → 7.4 hop
[SCENE] The import wall — logs 082 → 092 — eight `check` runs, eight different ImportErrors (modeladmin, wagtail.core, ugettext_lazy, StreamFieldPanel, BaseSetting, url, Query, BASE_URL). Speed-run them as a montage: that's what skipping 17 releases looks like. (B07–B14)
[SCENE] One command, 19 files — logs 084/085 — `wagtail updatemodulepaths` rewrites every wagtail.core import, even inside old migrations. Its help text still says "Update a Wagtail project tree to use Wagtail 2.x module paths". (B08)
[SCENE] **The migration that never came** — logs 093, 096, 097 — makemigrations: "no StreamField changes". migrate: 64 OK. Pages: 200. Then `EventPage.objects.filter(body__contains=…)` → `operator does not exist: text @> jsonb`. The body columns are still text, because the 3.0–5.x conversion migration is never generated if you skip those versions. Fixed with a hand-written ALTER … USING body::jsonb. (B15)
[SCENE] **Data lost by design** — logs 095, 102, 103 — the search log goes from 2 queries to 0. The migration that should have copied them has been a no-op since 6.0, with a comment saying you'd have run the real one on Wagtail 5. Recovered from the pre-upgrade dump. The strongest argument for "one release at a time". (B16)
[SCENE] Search got smarter — log 108 — "1 result for music" becomes "7 results": the only text difference across 51 pages. (B18)
[SCENE] The silent CSS regression — log 109 — STATICFILES_STORAGE is ignored on Django 5.1+, so no hashed filenames and no error. The comment in the 2019 settings file even warns about this "after a Wagtail upgrade". (B19)
[SCENE] Bold radio buttons — screenshots 2.7 vs 7.4 09-enrolment-form — Django 4.0 swapped <ul> for <div> in radio and checkbox widgets, and the 2019 CSS stopped matching. Found by pixel diff, fixed, and back to zero-pixel difference. (B21)
[SCENE] w-block- — rendered HTML `class="w-block-heading block-heading"` — 7.4 renames StreamField block classes and keeps the old ones for now. We switch the CSS before the old ones vanish. (B22)
[SCENE] ModelAdmin → PageListingViewSet — screenshots/2.7 vs 7.4 a10/a11 — the Events and Staff menus rebuilt on a new core API, same columns, same order. (B07)
[SCENE] The payoff — notes/screenshots/compare.md + log 127 — 11 of 13 front-end pages pixel-identical to 2019, byte-identical CSV exports, every submission present, zero deprecation warnings on Wagtail 7.4.
