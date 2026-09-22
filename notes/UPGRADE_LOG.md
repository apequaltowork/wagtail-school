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
- **Fix:** ac359b6 — committed the `forms/migrations/0002` AddField migration and added `Unidecode>=1.1,<2` to requirements.txt, with a comment explaining why. After that, `manage.py check` prints `forms.FormField: Added \ on 10 form field(s)` and `forms.ContactFormField: Added \ on 4 form field(s)` (log 053). All 14 clean_names now equal the stored 2.7 keys and match the data (log 054). The form, admin listing and CSV show every value again (log 055).
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
