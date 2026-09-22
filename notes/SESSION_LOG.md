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
