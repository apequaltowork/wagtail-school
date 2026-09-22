# Upgrade log

One entry per breakage.
Format: ID · hop · symptom (exact error, first lines + log file) · cause (which Wagtail/Django version changed what) · fix (commit + key before/after lines) · docs (versioned URL) · story value

---

# Hop 1: 2.7 → 2.15 LTS

## B01 — psycopg2-binary 2.8 won't install on Python 3.10
- **Hop:** 2.7 → 2.15
- **Symptom:** `pip install -r requirements.txt` → `Failed building wheel for psycopg2-binary` / `error: Microsoft Visual C++ 14.0 or greater is required.` (log 036)
- **Cause:** psycopg2-binary 2.8.x has no wheels for Python 3.10, so pip falls back to building from source, which needs MSVC and pg_config. Wagtail 2.15 is the first release that supports Python 3.10, which forces the Python bump.
- **Fix:** be3456d — `psycopg2-binary>=2.8,<2.9` → `psycopg2-binary>=2.9,<2.10`. The old line stays in requirements.txt, commented out with the reason. Installed 2.9.13 (log 037); pip check is clean (log 038).
- **Docs:** https://docs.wagtail.org/en/v2.15/releases/2.15.html (Python 3.10 support)
- **Story value:** Medium — the first wall is a database driver, not Wagtail.

## B02 — models.W042 on six models
- **Hop:** 2.7 → 2.15
- **Symptom:** `python -Wa manage.py check` → `core.SchoolSettings: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.`, plus the same for EventCategory, ContactFormField, FormField, HomePageQuickLink and Department. "System check identified 6 issues" (log 039).
- **Cause:** Django 3.2 added `DEFAULT_AUTO_FIELD` and warns when a project doesn't set it. Wagtail 2.15's own apps already declare `default_auto_field`, so only our apps warn.
- **Fix:** 99be2ab — added `DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'` to settings/base.py. This keeps the existing integer IDs, with no migrations. BigAutoField would mean an ALTER on every table for no benefit here. Check is clean (log 040).
- **Docs:** https://docs.djangoproject.com/en/3.2/releases/3.2/#customizing-type-of-auto-created-primary-keys
- **Story value:** Low — a common first sight on Django 3.2 upgrades, and a one-line fix.

## B03 — SiteMiddleware is gone from wagtail.core
- **Hop:** 2.7 → 2.15
- **Symptom:** the first request fails while loading middleware: `ModuleNotFoundError: No module named 'wagtail.core.middleware'` (log 045). `manage.py check` stays green, because middleware only loads on the first request.
- **Cause:** Wagtail 2.9 deprecated `SiteMiddleware` and `request.site` because they clash with Django's sites framework. 2.11 moved the middleware to `wagtail.contrib.legacy.sitemiddleware`, so the old path no longer exists.
- **Fix:** 075e7e5 — removed `'wagtail.core.middleware.SiteMiddleware'` from MIDDLEWARE. In `core/templatetags/navigation_tags.py`: `root = request.site.root_page` → `root = Site.find_for_request(request).root_page`. Pages return 200 again (log 046). The alternative (DECISIONS D14) is `wagtail.contrib.legacy.sitemiddleware.SiteMiddleware`.
- **Docs:** https://docs.wagtail.org/en/v2.15/releases/2.9.html#sitemiddleware-and-request-site-deprecated · https://docs.wagtail.org/en/v2.15/releases/2.11.html
- **Story value:** High — a classic "checks pass, site 500s" upgrade trap.

## B04 — Every form submission goes blank (the clean_name moment)
- **Hop:** 2.7 → 2.15
- **Symptom, in three stages:**
  1. After `migrate`, all 14 form fields have `clean_name = ''` (log 044). The 2.10 field is added by a plain `AddField(default='')`, with no data migration.
  2. On a server that never runs system checks (any WSGI server; log 048): **the 10-field enrolment form renders as a single field named `""`**, the admin submissions listing shows none of the stored values, and the CSV export has ten columns all headed "Subscribe to our newsletter", every value `None`. The data is still in the database but unreachable.
  3. `manage.py check` is meant to repair this (Wagtail backfills blank clean_names inside a *system check*), but it crashes (log 049):
     `Exception: You have form submission data that was created on an older version of Wagtail and requires the unidecode library to retrieve it correctly. Please install the unidecode package.`
- **Cause:** 2.10 made the submission key a stored `clean_name` field, generated with `safe_snake_case` / anyascii (`parentguardians_full_name`) instead of 2.7's on-the-fly `slugify(unidecode(label))` (`parentguardians-full-name`). For existing fields, `AbstractFormField.check()` → `_migrate_legacy_clean_name()` fills blanks with the legacy slug, which needs `unidecode`. Wagtail itself stopped depending on Unidecode (it was a 2.7 dependency), so a fresh 2.15 environment doesn't have it.
- **Fix:** ac359b6 — committed the `forms/migrations/0002` AddField migration and added `Unidecode>=1.1,<2` to requirements.txt, with a comment explaining why. After that, `manage.py check` prints "forms.FormField: Added `clean_name` on 10 form field(s)" and "forms.ContactFormField: Added `clean_name` on 4 form field(s)" (log 053). All 14 clean_names now equal the stored 2.7 keys and match the data (log 054). The form, admin listing and CSV show every value again (log 055).
- **Deploy lesson:** run `manage.py check` (or `migrate`, which runs checks, *twice*) on the server after deploying. Until something runs system checks, the live forms are broken.
- **Watch next:** a field added *after* the upgrade gets a snake_case key (`parentguardians_full_name`), so the enquiry form would end up mixing hyphenated and underscored keys (log 055).
- **Docs:** https://docs.wagtail.org/en/v2.15/releases/2.10.html#clean-name-field-added-to-form-builder-form-field-models
- **Story value:** High — the headline of this hop. Checks pass, the site runs, and every enquiry form quietly loses its data.

## B05 — Admin CSV export URL changed (?action=CSV is ignored)
- **Hop:** 2.7 → 2.15
- **Symptom:** `GET /admin/forms/submissions/<id>/?action=CSV` returns `200 text/html`, the normal listing page, instead of a CSV download (log 048). tools/baseline.py would have saved HTML as the "CSV".
- **Cause:** the form submissions listing now uses `wagtail.admin.views.mixins.SpreadsheetExportMixin`, which reads `?export=csv` or `?export=xlsx`. The old parameter is silently ignored. I couldn't find this in the 2.8–2.15 upgrade considerations; I verified it in the 2.15 source (`wagtail/contrib/forms/views.py`, `SubmissionsListView.is_export`).
- **Fix:** 411af7e — tools/baseline.py tries `?export=csv` first, falls back to `?action=CSV`, and fails if neither returns text/csv.
- **Docs:** https://docs.wagtail.org/en/v2.15/reference/contrib/forms/index.html
- **Story value:** Medium — an undocumented URL change that breaks bookmarks, scripts and tooling, and fails silently.

## B06 — seed_demo: get_document_model moved
- **Hop:** 2.7 → 2.15
- **Symptom:** `seed_demo` on a fresh 2.15 database → `ImportError: cannot import name 'get_document_model' from 'wagtail.documents.models'` (log 059). The running site isn't affected; only the management command imports it.
- **Cause:** Wagtail 2.8 moved `get_document_model` to `wagtail.documents`. The old location went away after the deprecation period.
- **Fix:** 784a595 — `from wagtail.documents.models import get_document_model` → `from wagtail.documents import get_document_model`. Seeding from empty now gives the same counts as 2.7 (log 060).
- **Docs:** https://docs.wagtail.org/en/v2.15/releases/2.8.html#wagtail-documents-models-get-document-model-has-moved
- **Story value:** Low — it only surfaces because we reseed from scratch; that's why you keep a clean-DB check in the upgrade.


---

# Hop 2: 2.15 → 7.4 LTS (one step)

Install went through on the first try (log 080: wagtail 7.4.3, Django 5.2.17, Pillow 12.3.0, psycopg2-binary 2.9.13; pip check clean in 081). Then `python -Wa manage.py check` failed eight times in a row, each time on the first import it couldn't resolve. The one-step jump means every removal from 3.0 to 6.0 shows up as a hard ImportError, with no deprecation warning first.

## B07 — ModelAdmin is gone
- **Hop:** 2.15 → 7.4
- **Symptom:** `ModuleNotFoundError: No module named 'wagtail.contrib.modeladmin'` (log 082), raised from INSTALLED_APPS before anything else loads.
- **Cause:** `wagtail.contrib.modeladmin` was deprecated in 5.1 and removed in 6.0. It lives on as the external `wagtail-modeladmin` package.
- **Fix:** d48278c — removed the app. `events/wagtail_hooks.py` and `staff/wagtail_hooks.py` now register a `PageListingViewSet` (`wagtail.admin.viewsets.pages`) through `register_admin_viewset`. It keeps the same menu labels, icons and order, with `list_display` / `list_filter` in place of ModelAdmin's. The listing screens are verified in the admin screenshots. Alternative (DECISIONS D23): the `wagtail-modeladmin` package.
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/6.0.html · https://docs.wagtail.org/en/v7.4/reference/viewsets.html
- **Story value:** High — the admin menus the client uses every day have to be rebuilt on a new API.

## B08 — wagtail.core no longer exists
- **Hop:** 2.15 → 7.4
- **Symptom:** `ModuleNotFoundError: No module named 'wagtail.core'` (log 083).
- **Cause:** Wagtail 3.0 moved `wagtail.core.*` to `wagtail.*` and `wagtail.admin.edit_handlers` to `wagtail.admin.panels`, with shims that 5.0 removed. None of it warned on 2.15 (see deprecations-2.15.txt).
- **Fix:** ee0e4c1 — ran Wagtail's own `wagtail updatemodulepaths .` (preview in log 084, apply in 085). It rewrote 19 files and 42 lines, including the old migrations and `'wagtail.core'` → `'wagtail'` in INSTALLED_APPS. Its help text still says "Update a Wagtail project tree to use Wagtail 2.x module paths". It does **not** replace removed panel classes, and it leaves `wagtail.images.edit_handlers` / `wagtail.snippets.edit_handlers` alone (B10).
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/3.0.html
- **Story value:** High — the biggest diff of the upgrade, done by one command.

## B09 — ugettext_lazy removed
- **Hop:** 2.15 → 7.4
- **Symptom:** `ImportError: cannot import name 'ugettext_lazy' from 'django.utils.translation' … Did you mean: 'gettext_lazy'?` (log 086).
- **Cause:** deprecated in Django 3.0, removed in 4.0. It warned 60+ times on 2.15.
- **Fix:** 08e310e — `ugettext_lazy as _` → `gettext_lazy as _` in 7 files.
- **Docs:** https://docs.djangoproject.com/en/5.2/releases/4.0/#features-removed-in-4-0
- **Story value:** Low — Python suggests the fix itself.

## B10 — StreamFieldPanel and the chooser panels removed
- **Hop:** 2.15 → 7.4
- **Symptom:** `ImportError: cannot import name 'StreamFieldPanel' from 'wagtail.admin.panels' … Did you mean: 'TitleFieldPanel'?` (log 087).
- **Cause:** 3.0 folded `StreamFieldPanel`, `ImageChooserPanel`, `DocumentChooserPanel` and `SnippetChooserPanel` into `FieldPanel`; 5.0 removed them, along with `wagtail.images.edit_handlers` and `wagtail.snippets.edit_handlers`.
- **Fix:** dffbf43 — 9 panels → `FieldPanel(...)`, and the imports from the `images` and `snippets` `edit_handlers` modules removed. `PageChooserPanel` still exists and stays.
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/3.0.html · https://docs.wagtail.org/en/v7.4/releases/5.0.html
- **Story value:** Medium — the code gets simpler: one panel type instead of five.

## B11 — BaseSetting removed
- **Hop:** 2.15 → 7.4
- **Symptom:** `ImportError: cannot import name 'BaseSetting' from 'wagtail.contrib.settings.models' … Did you mean: 'BaseSiteSetting'?` (log 088).
- **Cause:** 4.0 split settings into `BaseSiteSetting` (per site) and `BaseGenericSetting` (global); 5.0 removed `BaseSetting`.
- **Fix:** 72279ff — `SchoolSettings(BaseSetting)` → `SchoolSettings(BaseSiteSetting)`. That's the per-site behaviour we already had, so templates using `settings.core.SchoolSettings` don't change.
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/4.0.html
- **Story value:** Low.

## B12 — django.conf.urls.url removed
- **Hop:** 2.15 → 7.4
- **Symptom:** `ImportError: cannot import name 'url' from 'django.conf.urls'` (log 089).
- **Cause:** deprecated in Django 3.1, removed in 4.0.
- **Fix:** b2fe321 — `from django.conf.urls import include, url` → `from django.urls import include, re_path`, with every `url(` → `re_path(`, so the regexes are unchanged. The smallest change; converting to `path()` would be a rewrite.
- **Docs:** https://docs.djangoproject.com/en/5.2/releases/4.0/#features-removed-in-4-0
- **Story value:** Low.

## B13 — Search Query model moved
- **Hop:** 2.15 → 7.4
- **Symptom:** `ImportError: cannot import name 'Query' from 'wagtail.search.models'` (log 090), raised from the 2.7 project template's `search/views.py`.
- **Cause:** 5.0 moved `Query` and `QueryDailyHits` to `wagtail.contrib.search_promotions`; 6.0 removed them from `wagtail.search`.
- **Fix:** d3c6926 — added `'wagtail.contrib.search_promotions'` to INSTALLED_APPS; `from wagtail.search.models import Query` → `from wagtail.contrib.search_promotions.models import Query`. Whether the 2 logged queries survive is checked after migrate. Alternative (D24): drop query logging, as the current template does.
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/5.0.html · https://docs.wagtail.org/en/v7.4/releases/6.0.html
- **Story value:** Medium — even the file `wagtail start` generated for you breaks.

## B14 — BASE_URL renamed (wagtailadmin.W003)
- **Hop:** 2.15 → 7.4
- **Symptom:** once the app loads: `?: (wagtailadmin.W003) The WAGTAILADMIN_BASE_URL setting is not defined` (log 091).
- **Cause:** 3.0 renamed `BASE_URL` to `WAGTAILADMIN_BASE_URL`; 5.0 stopped reading the old name.
- **Fix:** 8c1d046 — `BASE_URL = 'http://localhost:8000'` → `WAGTAILADMIN_BASE_URL = 'http://localhost:8074'` (this stage's port). Check is clean, with no Python warnings (log 092).
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/3.0.html
- **Story value:** Low.

## B15 — StreamField columns silently stay text (the migration that never came)
- **Hop:** 2.15 → 7.4
- **Symptom:** nothing errors. `makemigrations` finds **no** StreamField changes, only 8 form-field AlterFields (log 093), and `migrate` runs 64 migrations cleanly (log 095). Wagtail's own migrations convert revisions, log entries and `form_data` to `jsonb`, but our three `body` columns stay `text` (logs 094 vs 096). Pages still render with 200, but any JSON query on a StreamField fails (log 097):
  `ProgrammingError: operator does not exist: text @> jsonb`
- **Cause:** Wagtail 3.0 introduced `use_json_field=True`; adding it generated an `AlterField` that converted the column to jsonb, and Wagtail 5.0 made it mandatory ("Wagtail 5.0 required older TextField-based streams to be migrated"). From 6.0, `use_json_field` is "ignored, but retained for compatibility with historical migrations" and isn't deconstructed, so Django sees no difference between the 2.7-era migration and the 7.4 model. A project that jumps from 2.x straight to 6.0+ never gets the conversion. A fresh 7.4 database creates `jsonb`, and this one keeps `text`: schema drift that no tool reports.
- **Fix:** c22c712 — hand-written `RunSQL` migrations `home.0004`, `pages.0002` and `events.0002`: `ALTER TABLE … ALTER COLUMN body TYPE jsonb USING body::jsonb` (reversible; a no-op on databases already in jsonb; model state unchanged). All 24 bodies were valid JSON with no empty strings, so the cast needed no clean-up. Columns are now jsonb (log 099), the JSON query returns 2, the two Open Day events that carry a call to action (log 100), and `makemigrations --check` is clean (log 101).
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/3.0.html · https://docs.wagtail.org/en/v7.4/releases/5.0.html · https://docs.wagtail.org/en/v7.4/releases/6.0.html
- **Story value:** High — the scariest kind of upgrade bug: green checks, working pages, and a database that doesn't match the code.

## B16 — Logged search queries lost in the jump
- **Hop:** 2.15 → 7.4
- **Symptom:** after `migrate`, `wagtailsearchpromotions_query` and `…_querydailyhits` are empty: "after migrate: queries = 0, daily hits = 0" (log 102). The restored 2.15 data had 2 queries ("music", "scholarship") with daily hits. The migrate log shows `wagtailsearch.0008_remove_query_and_querydailyhits_models` dropping the old tables, and `wagtailsearchpromotions.0004_copy_queries` "OK" without copying anything (log 095).
- **Cause:** the Query model moved to `wagtail.contrib.search_promotions` in 5.0, whose `0004_copy_queries` copied the rows. In 6.0 that migration was **changed to a no-op**. Its source comment says any project needing the copy "would have already applied the real version of this migration while they were running Wagtail 5". Skipping Wagtail 5 means `0008` drops the tables with nothing copied. This is the direct cost of the one-step jump (DECISIONS D21).
- **Fix:** 793b60c — `tools/recover_search_queries.py` reads `wagtailsearch_query` and `wagtailsearch_querydailyhits` out of the pre-upgrade dump (`pg_restore --data-only -t …`) and recreates them through the search_promotions models. Result: 2 queries and 2 daily-hit rows, "music" 9 hits and "scholarship" 5 (log 103). In a real project: take the dump before migrating, or pass through Wagtail 5.x once for this app.
- **Docs:** https://docs.wagtail.org/en/v7.4/releases/5.0.html · https://docs.wagtail.org/en/v7.4/releases/6.0.html (and the comment in `wagtail/contrib/search_promotions/migrations/0004_copy_queries.py`)
- **Story value:** High — real data loss from skipping versions, and it's documented only in a code comment.
