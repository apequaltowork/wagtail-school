# Session log — 2.7 build

## 2026-09-22 09:26 — Step 1: project rules and logging tools
- **What:** created `D:\django\wagtail-school` with CLAUDE.md, bin/rec, notes/ (SESSION_LOG, SCENES, DECISIONS), .gitignore and .gitattributes.
- **Why:** the rules and logging have to exist before the first command, so that every command after this one gets recorded.
- **Log:** none (no commands run yet).
- **Result:** done. Git is not initialised until the scaffold exists.

## 2026-09-22 09:30 — Step 2: Python 3.8, virtualenv, Wagtail 2.7 scaffold
- **What:** installed uv, then CPython 3.8.20 through uv; created the `wagtail-school` virtualenv; installed wagtail 2.7.4, Django 2.2.28 and psycopg2-binary 2.8.6; ran `wagtail start schoolsite` into the existing folder; ran git init and made the first commit.
- **Why:** Wagtail 2.7 supports Python 3.5–3.8, and only 3.12 was installed.
- **Logs:** 001-install-uv, 002-uv-python-38 (exit 2), 003-mkvirtualenv, 004-pip-install-wagtail27, 005-wagtail-start.
- **Result:** OK. uv exited with code 2 while creating its `cpython-3.8` minor-version link on Windows, but the interpreter itself installed fine, so the full 3.8.20 path is used. The first `.gitignore` had an unanchored `static/` that hid the template's app static folders; this was fixed in commit 2a9c53d.

## 2026-09-22 09:40 — Step 3 (in progress): PostgreSQL and site code
- **What:** wrote the gitignored settings/local.py (Postgres, `school` role, generated password and SECRET_KEY). Vendored Bootstrap 4.4.1, jQuery 3.4.1, Popper 1.16.0 and the Merriweather / Source Sans Pro woff2 files (npm pack, with the owner's approval). Wrote the models, templates and CSS for core, home, pages, events, staff and forms, the Pillow asset generator and the seed_demo command.
- **Logs:** 006-check (clean), 007-makemigrations (exit 1: Django 2.2 needs a live DB for its migration-history check, and the `school` role isn't created yet), 008-make-assets.
- **Result:** waiting for the owner to create the Postgres role and database.

## 2026-09-22 10:15 — Step 3: database, migrations, seed
- **What:** the owner created role `school` and database `wagtail_school`. I ran makemigrations and migrate, checked that makemigrations --check reports no changes, then ran seed_demo.
- **Logs:** 009-makemigrations-2, 010-migrate, 011-makemigrations-check, 012-seed-demo-1 (exit 1), 013–015 seed runs, 016-recreate-db, 017-migrate-fresh, 018/019 seed-fresh.
- **Result:** run 012 failed with `UnicodeEncodeError: 'charmap' codec can't encode character '\u0101'`. The console email backend wrote an enquiry containing "Te reo Māori" to a piped stdout, which Windows encodes as cp1252. Fixed in bin/rec with `PYTHONUTF8=1`; the site code didn't change. The failed run also left 26 orphaned media files (the DB rolled back but the files were already written), so tools/recreate_db.py now drops and recreates the DB and empties media/. From an empty DB: migrate → seed_demo --reset → seed_demo --reset both succeeded, giving 43 live pages, 26 images, 3 documents, 5 categories, 9 departments and 30 + 10 submissions. A plain `seed_demo` on existing content exits 0 with a message.

## 2026-09-22 10:20 — Step 4: crawl, fixes, screenshots
- **What:** trial crawl with tools/baseline.py, then Playwright screenshots (tools/screenshots/shoot.js, Node Playwright in its own folder).
- **Result:** the crawl found `/search/` returning 500. `includes/page_banner.html` used `{{ title|default:page.title }}`, and Django resolves the filter argument even when `title` is set, so a view without `page` in context raised VariableDoesNotExist (fixed in 6189150). The screenshots showed stretched event cards, because `{% image %}` writes height="360" and Bootstrap's `.card-img-top` sets only the width (fixed in 66d9b15). Final screenshots: 13 front end + thank-you, and 16 admin, in notes/screenshots/2.7/ (log 021).

## 2026-09-22 10:24 — Step 5: baseline, dump
- **What:** seed_demo --reset (to drop the screenshot test submission), then baseline/ via tools/baseline.py, pip freeze, pg_dump -Fc and the media zip.
- **Logs:** 022-seed-for-baseline, 023-baseline-2.7, 024-pip-freeze, 025-pg-dump-27, 026-zip-media-27, 027-baseline-selfcheck (all six files identical on a second run).
- **Result:** 55 URLs (54 × 200, 1 × 404 by design), text for 51 HTML pages, 43 pages across 8 types, 26 images, 3 documents, 5 + 9 snippets, and 30 + 10 submissions. The form keys are 2.7's hyphenated slugs (`parentguardians-full-name`, `languages-spoken-at-home-eg-francais-espanol`). dumps/wagtail_school_27.dump is 215 KB and dumps/media_27.zip is 2.5 MB.

## 2026-09-22 10:26 — Step 6: final checks
- **Logs:** 028-final-check-Wa (no issues; Python 3.8 prints two DeprecationWarnings from the 2.7 stack itself), 029-final-makemigrations-check (no changes), 030 showmigrations (95 applied, 0 pending).
- **Result:** done. README written; tagged v2.7-baseline.
