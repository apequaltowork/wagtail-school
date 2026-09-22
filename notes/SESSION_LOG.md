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

---

# Session log — 2.7 → 2.15 hop

## 2026-09-22 10:45 — Setup
- **What:** cloned wagtail-school into wagtail-school-215 on branch `upgrade/2.15`. Installed CPython 3.10.21 through uv (the same Windows minor-version link error as for 3.8; the interpreter is fine) and created the `wagtail-school-215` virtualenv. Created `wagtail_school_215` as the `school` role, which has CREATEDB, so no superuser was needed. Restored `wagtail_school_27.dump` with `pg_restore --no-owner --no-privileges`, unzipped media_27.zip, and wrote a new gitignored settings/local.py with its own SECRET_KEY.
- **Why:** each stage gets its own folder, virtualenv and database; the 2.7 stage stays untouched.
- **Logs:** 031-uv-python-310 (exit 2, harmless), 032-mkvirtualenv-215, 033-createdb-215, 034-pg-restore-27-into-215, 035-unzip-media-27.
- **Result:** the restored DB has 44 page rows (including root), 40 form submissions and 26 original images. Nothing is installed in the new virtualenv yet.

## 2026-09-22 10:50 — Plan approved
- Read the upgrade considerations for 2.8–2.15. The plan and the SiteMiddleware choice (owner: replace it) are in DECISIONS D13–D15.

## 2026-09-22 10:55 — Dependencies (B01)
- Bumped to Django>=3.2,<3.3 and wagtail>=2.15,<2.16. psycopg2-binary 2.8 failed to build on Python 3.10 (log 036), so it's now 2.9, with the old line commented out. Installed wagtail 2.15.6, Django 3.2.25, psycopg2-binary 2.9.13 and Pillow 9.5.0. pip check is clean (log 038).

## 2026-09-22 11:00 — Checks and middleware (B02, B03)
- `-Wa check` showed six models.W042 warnings (log 039) → DEFAULT_AUTO_FIELD = AutoField (log 040 clean).
- A request made without system checks crashed with ModuleNotFoundError 'wagtail.core.middleware' (log 045) → SiteMiddleware removed, and the menu tag now uses Site.find_for_request (log 046).

## 2026-09-22 11:05 — Migrations and the clean_name investigation (B04, B05)
- makemigrations: `forms.0002` adds clean_name to both form-field models (log 041). migrate on the restored data: OK (log 042).
- After migrate, all 14 clean_names were blank (log 044). Without system checks, the enrolment form rendered as one field named "" and the admin and CSV lost every value (log 048). `?action=CSV` returned HTML (B05).
- `manage.py check` crashed because the legacy backfill needs unidecode (log 049) → added Unidecode to requirements. check then backfilled 10 + 4 clean_names with the 2.7 hyphenated keys (log 053), and every value is back (logs 054, 055).
- tools/baseline.py now exports with `?export=csv`.

## 2026-09-22 11:15 — Clean-database check (B06, D16)
- On a throwaway `wagtail_school_215_fresh`, migrate succeeded (log 057); the homepage migration happened to run before 0053_locale_model, and I added `run_before` anyway (D16). seed_demo failed on the `get_document_model` import (log 059) → fixed (log 060). A fresh seed stores snake_case keys (log 061, D18). The throwaway DB was dropped and media/ restored from media_27.zip.

## 2026-09-22 11:25 — Verification
- Crawl against runserver on port 8215 compared with the 2.7 baseline: all six files identical, byte for byte (log 062; final rerun log 072). That covers URL statuses, page text for 51 pages, counts, form field keys and both admin CSV exports.
- Screenshots in notes/screenshots/2.15 (logs 063, 065). The 12 front-end pages are pixel-identical to 2.7; the 404 differs only in Django 3.2's debug page. Admin screenshots are now taken at full document height, because 2.15's fixed sidebar and footer broke fullPage stitching. The screenshot test submission was deleted (log 064; its keys were the hyphenated 2.7 ones).
- 18 remaining deprecation warnings are in notes/deprecations-2.15.txt, plus the known 3.0+ changes that don't warn on 2.15.
- Final checks: pip check (068), check (069), makemigrations --check (070) and migrate (071) all clean. pip freeze saved to notes/check-2.15/pip-freeze.txt.
- dumps/wagtail_school_215.dump (301 KB) and dumps/media_215.zip (2.5 MB). Tagged v2.15.
