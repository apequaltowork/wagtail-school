# Decisions

Every non-obvious choice, and why.

## D01 — Windows adaptations of the brief
The brief was written for Linux/Mac (`~/Desktop/django`, `sudo -u postgres`, POSIX virtualenvwrapper). This machine is Windows 10, so:
- Project root is `D:\django\wagtail-school` (renamed from `wagtail-school-demo` at the owner's request). Virtualenv and database names follow: `wagtail-school` / `wagtail_school`, and later `-215` / `-74`.
- Python 3.8 comes from `uv python install 3.8` (only 3.12 was installed). The virtualenv is made with virtualenvwrapper-win (`mkvirtualenv -p`), and binaries live under `Scripts\` rather than `bin/`.
- PostgreSQL 16 is a native Windows install. Superuser admin work (`psql -U postgres`) is run by the owner, which replaces `sudo -u postgres`. The app role owns its database and has CREATEDB so the Django test runner works.
- `bin/rec` is a bash script run under Git Bash. `.gitattributes` keeps it LF.

## D02 — School name
A web search for "Kestrel Ridge College" found no school by that name. The closest hit was a US communications consultancy, "Kestrel Ridge Education & Communication Developers", which is not a school. The name is kept, with a fictional suburb, "Kestrel Ridge, NSW", and a fictional founding year, 1962.

## D03 — Commit authorship
Commits are authored by the channel owner, with no AI attribution trailers. The repo history is part of the public video.

## D04 — `static/` in .gitignore
The brief says to ignore collected static output. `wagtail start` keeps source static files in `schoolsite/static/`, and `collectstatic` writes to `<root>/static/`. So only the root `/static/` is ignored (anchored), and `schoolsite/static/` (Bootstrap, CSS, fonts) is committed.

## D05 — PYTHONUTF8=1 in bin/rec
Windows pipes stdout as cp1252, so Django's console email backend crashed on non-ASCII form answers (log 012). The fix belongs in the environment, not the code: bin/rec exports `PYTHONUTF8=1`. Run by hand on Windows, set the same variable.

## D06 — Embed block is defined but not seeded
`BaseStreamBlock` includes `embed` (EmbedBlock), as the brief asks. Seeding it would mean embedding a real third-party video and fetching oEmbed over the network at render time, which conflicts with "fictional, no downloads" and makes the page-text baseline depend on the network. It stays available in the editor.

## D07 — StreamFields render with `{{ page.body }}`
This is the 2.7 idiom, and it wraps each block in `<div class="block-<type>">`. The CSS targets those wrapper classes (`.block-quote blockquote`, `.block-table table` …), the way a 2019 site typically did, so any change to the wrapper markup in later Wagtail versions will show up in the screenshots.

## D08 — Seed file naming and resets
`seed_demo --reset` deletes the pages under Home, then images, documents, snippets, settings and submissions, in its own transaction. Wagtail's post_delete handlers remove the files on commit, then the rebuild runs in a second transaction. Submissions are created in a shuffled order (fixed seed 2019) so enquiry and contact submissions interleave, and submit_time is then assigned in pk order across the last 182 days.

## D09 — `data-baseline="dynamic"`
Listings whose content depends on today's date (upcoming and past events, the home page's next three events, the "already taken place" note) carry `data-baseline="dynamic"`. The page-text baseline strips those elements, so a later stage run on a different day still compares like with like.

## D10 — Baseline and screenshot order
The thank-you screenshot has to submit the enrolment form. So the order is: seed → screenshots (admin first, then front end and the POST) → seed --reset → baseline → dump. The baseline and the dump both hold exactly 30 + 10 seeded submissions, while the screenshots show the same content (same seed, same day).

## D11 — Tooling reads the DB through Django
tools/baseline.py, screenshot_targets.py and dump_db.py call django.setup() and resolve page IDs and credentials at run time, with import fallbacks for `wagtail.models` (3.0+) and `wagtail.documents.get_document_model` (2.8+). The same tools should run on every stage with at most small edits, and any edits are logged as part of that hop.

## D12 — Dev SECRET_KEY left in dev.py
`wagtail start` 2.7 writes a development SECRET_KEY into settings/dev.py. It is kept, because the brief says to keep everything the template generates. It's a throwaway dev key, and local.py overrides it with a private one.

---

# 2.7 → 2.15 hop

## D13 — Stop at 2.15 LTS first
2.15 is the LTS release that includes the 2.10 form-builder change (`clean_name`). Stopping here applies that change to real restored 2.7 submissions before the big jump to 7.4.

## D14 — Replace SiteMiddleware with Site.find_for_request (owner's choice)
2.9 deprecated `SiteMiddleware` and `request.site`; 2.11 moved the middleware to `wagtail.contrib.legacy.sitemiddleware`. The smallest change would be to point MIDDLEWARE at the legacy path. The owner chose the path the release notes recommend instead: drop the middleware and call `Site.find_for_request(request)` in the menu tag. **Alternative:** the legacy middleware, which keeps `request.site` for one more hop. Docs: https://docs.wagtail.org/en/v2.15/releases/2.9.html

## D15 — Leave deprecation warnings for the 7.4 hop
`ugettext_lazy`, `url()`, `wagtail.core.*` imports, `classname=` on blocks, the `db` search backend and the `search()` partial-match warning all still work on 2.15, so they are recorded in notes/deprecations-2.15.txt rather than fixed.

## D16 — run_before on the homepage migration (applied without a failure)
The 2.11 upgrade considerations say the initial homepage migration from the old project template needs `run_before = [('wagtailcore', '0053_locale_model')]`. On a fresh database, `migrate` still succeeded without it (log 057). `home.0001` depends only on `wagtailcore.0040`, so Django's planner happened to run `home.0002` before `0053`. Nothing failed, but that ordering is luck, not a guarantee, and the setting is harmless on an already-migrated database. So I added it anyway, following the docs (16399a1). It isn't in UPGRADE_LOG because nothing broke.
Docs: https://docs.wagtail.org/en/v2.15/releases/2.11.html

## D17 — Fresh-DB check uses a throwaway database
The gitignored settings/local.py reads `DB_NAME` from the environment (default `wagtail_school_215`), so migrations and seeding from empty can be tested on `wagtail_school_215_fresh` without touching the restored data. The throwaway DB is dropped after use.

## D18 — Two key styles in one database
A form created on 2.15 (fresh seed) stores snake_case keys (`parentguardians_full_name`, log 061). Forms carried over from 2.7 keep their hyphenated keys, backfilled by the legacy check. Both work. The restored database, the one that matters, keeps the 2.7 keys, so nothing is rewritten in the stored submissions.

## D19 — Screenshot capture method for the admin
From 2.15 the admin uses fixed-position sidebar and footer elements, which Playwright's fullPage stitching duplicates over the content. Admin shots now grow the viewport to the document height and take a single screenshot (tools/screenshots/shoot.js, `tall`). Front-end shots still use fullPage, so they stay comparable with 2.7.

## D20 — The 404 screenshot shows Django's debug page
With DEBUG=True, a 404 renders Django's technical page, not templates/404.html, on every stage, including the 2.7 baseline. The 2.7 stage is frozen, so this stays as it is. The 404 status is still verified by the crawler.
