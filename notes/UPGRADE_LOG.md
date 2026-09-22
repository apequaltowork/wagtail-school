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
