# Kestrel Ridge College — Wagtail 2.7 demo site

> **This folder is the 7.4 stage** (`wagtail-school-74`, branch `upgrade/7.4`, tag `v7.4`):
> Wagtail 7.4.3 LTS, Django 5.2 LTS, Python 3.12, database `wagtail_school_74`, runserver port 8074.
> Upgraded 2.7 → 2.15 → 7.4. Every breakage (B01–B22) is in `notes/UPGRADE_LOG.md`; screenshots
> side by side in `notes/screenshots/compare.md`. The ModelAdmin menus are now `PageListingViewSet`s,
> and search logging uses `wagtail.contrib.search_promotions`. The rest of this README describes the original 2.7 build.

A deliberately **period-accurate Wagtail 2.7 / Django 2.2 codebase** for a fictional Australian
K–12 school. It exists to be upgraded on camera for
*"I Upgraded Wagtail 2.7 → 7.4 — Everything That Broke"*.

The code is written the way a 2019 Wagtail project was written: `wagtail.core` imports,
`edit_handlers` panels (`StreamFieldPanel`, `ImageChooserPanel`, `SnippetChooserPanel` …),
text-stored StreamFields, `contrib.modeladmin`, `BaseSetting`, `SiteMiddleware` with `request.site`,
`url()` routes and `ugettext_lazy`. **Don't modernise it here.** The upgrades happen in their own
folders (`wagtail-school-215`, `wagtail-school-74`), each with its own virtualenv and database.

Everything is fictional: the school, the suburb, every person, every phone number (ACMA's
fictional `(02) 5550` range) and every email address (`.example`). The images and PDFs are drawn
with Pillow by `seed/make_assets.py`, so there are no photos of real people.

## What's in it

| App | What it does |
|---|---|
| `home` | HomePage with a hero, call to action, quick links (InlinePanel), a StreamField body and the next three events |
| `pages` | StandardPage: intro, hero image, StreamField body |
| `events` | EventCategory snippet, EventIndexPage (RoutablePageMixin: upcoming, paginated, `?category=`, `/past/`), EventPage, and the "Events" ModelAdmin |
| `staff` | Department snippet, StaffIndexPage (grouped, `?department=`), StaffPage, and the "Staff" ModelAdmin |
| `forms` | Enrolment Enquiry (FormPage) and Contact Us (ContactPage), both AbstractEmailForm with FormSubmissionsPanel |
| `core` | SchoolSettings (BaseSetting), shared StreamField blocks (heading, paragraph, image, quote, call to action, embed, document, table), menu and breadcrumb tags, `seed_demo` |
| `search` | the search view from the 2.7 project template (records `Query` hits) |

The front end uses Bootstrap 4.4.1, jQuery 3.4.1 and Popper 1.16, all vendored in `schoolsite/static/vendor`, with Merriweather and Source Sans Pro.

## Setup (Windows, as used for the video)

Requirements: Python 3.8 (via `uv python install 3.8`), virtualenvwrapper-win, PostgreSQL 16.

```bat
mkvirtualenv -p <path to python 3.8> wagtail-school
%WORKON_HOME%\wagtail-school\Scripts\pip install -r requirements.txt
```

Create the database as the postgres superuser:

```sql
CREATE ROLE school LOGIN CREATEDB PASSWORD '<choose one>';
CREATE DATABASE wagtail_school OWNER school ENCODING 'UTF8';
```

Create `schoolsite/settings/local.py`. It's gitignored and never committed:

```python
SECRET_KEY = '<random>'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': 'wagtail_school',
                         'USER': 'school', 'PASSWORD': '<password>', 'HOST': 'localhost', 'PORT': '5432'}}
```

Then migrate and seed:

```bat
set PYTHONUTF8=1
set DEMO_ADMIN_PASSWORD=kestrel-demo-2019
python manage.py migrate
python manage.py seed_demo --reset
python manage.py runserver 8027
```

`seed_demo` builds the page tree (43 live pages), 26 images, 3 PDFs, snippets, settings, and
30 + 10 form submissions created through Wagtail's own `get_form()` / `process_form_submission()`.
`--reset` deletes the demo content and rebuilds it. `PYTHONUTF8=1` matters on Windows: the console
email backend prints the submissions, and some contain non-ASCII answers.

## Demo login

<http://127.0.0.1:8027/admin/>, user **admin**, password **kestrel-demo-2019**. That's a local demo
password only, set through `DEMO_ADMIN_PASSWORD`.

## Upgrade tooling

| Path | Purpose |
|---|---|
| `bin/rec <slug> <cmd…>` | runs a command and logs its full output to `notes/logs/NNN-<slug>.log` |
| `tools/baseline.py` | crawls the running site and writes `baseline/`, or compares against it with `--compare baseline` |
| `tools/screenshots/shoot.js` | Playwright full-page screenshots (`npm install` in that folder first) |
| `tools/dump_db.py` | `pg_dump -Fc` using the local.py credentials |
| `tools/recreate_db.py --yes` | drops and recreates the database and empties `media/` |

`baseline/` holds the 2.7 reference: URL statuses, page text, counts, the admin's CSV exports and
the form field keys. The DB dump and media zip live in `dumps/`, which is gitignored:
`wagtail_school_27.dump` and `media_27.zip`.

`notes/` is the raw material for the video: `SESSION_LOG.md`, `SCENES.md`, `DECISIONS.md`,
`logs/` and `screenshots/2.7/`. Project rules for every session are in `CLAUDE.md`.
