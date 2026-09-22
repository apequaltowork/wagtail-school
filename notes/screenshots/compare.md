# Screenshots: 2.7 → 2.15 → 7.4

Full-page screenshots at 1366px wide, taken by `tools/screenshots/shoot.js` on each stage.
Front-end pages are compared pixel for pixel between 2.7 and 7.4. Admin screens differ by design
(a new admin UI), so the notes say what changed.

| Screen | 2.7 | 2.15 | 7.4 | 2.7 vs 7.4 | Notes |
|---|---|---|---|---|---|
| `01-home` | [2.7](2.7/01-home.png) | [2.15](2.15/01-home.png) | [7.4](7.4/01-home.png) | **pixel-identical** |  |
| `02-standard-page` | [2.7](2.7/02-standard-page.png) | [2.15](2.15/02-standard-page.png) | [7.4](7.4/02-standard-page.png) | **pixel-identical** |  |
| `03-fees` | [2.7](2.7/03-fees.png) | [2.15](2.15/03-fees.png) | [7.4](7.4/03-fees.png) | **pixel-identical** |  |
| `04-events-index` | [2.7](2.7/04-events-index.png) | [2.15](2.15/04-events-index.png) | [7.4](7.4/04-events-index.png) | **pixel-identical** |  |
| `05-event-detail` | [2.7](2.7/05-event-detail.png) | [2.15](2.15/05-event-detail.png) | [7.4](7.4/05-event-detail.png) | **pixel-identical** |  |
| `06-past-events` | [2.7](2.7/06-past-events.png) | [2.15](2.15/06-past-events.png) | [7.4](7.4/06-past-events.png) | **pixel-identical** |  |
| `07-staff-index` | [2.7](2.7/07-staff-index.png) | [2.15](2.15/07-staff-index.png) | [7.4](7.4/07-staff-index.png) | **pixel-identical** |  |
| `08-staff-detail` | [2.7](2.7/08-staff-detail.png) | [2.15](2.15/08-staff-detail.png) | [7.4](7.4/08-staff-detail.png) | **pixel-identical** |  |
| `09-enrolment-form` | [2.7](2.7/09-enrolment-form.png) | [2.15](2.15/09-enrolment-form.png) | [7.4](7.4/09-enrolment-form.png) | **pixel-identical** | Identical after B21 (Django 4.0 widget markup); before the fix the options rendered bold. |
| `10-form-thank-you` | [2.7](2.7/10-form-thank-you.png) | [2.15](2.15/10-form-thank-you.png) | [7.4](7.4/10-form-thank-you.png) | **pixel-identical** |  |
| `11-contact` | [2.7](2.7/11-contact.png) | [2.15](2.15/11-contact.png) | [7.4](7.4/11-contact.png) | **pixel-identical** |  |
| `12-search-results` | [2.7](2.7/12-search-results.png) | [2.15](2.15/12-search-results.png) | [7.4](7.4/12-search-results.png) | differs (size 1366×954 → 1366×1730) | Expected difference (B18): the `database` search backend finds 7 results for "music" instead of 1. |
| `13-not-found` | [2.7](2.7/13-not-found.png) | [2.15](2.15/13-not-found.png) | [7.4](7.4/13-not-found.png) | differs in region (0, 15, 1366, 342) | Django's DEBUG 404 page on every stage (D20); only the debug page's own layout differs. |
| `a01-dashboard` | [2.7](2.7/a01-dashboard.png) | [2.15](2.15/a01-dashboard.png) | [7.4](7.4/a01-dashboard.png) | new admin UI |  |
| `a02-edit-home-page` | [2.7](2.7/a02-edit-home-page.png) | [2.15](2.15/a02-edit-home-page.png) | [7.4](7.4/a02-edit-home-page.png) | new admin UI | New editor UI (Wagtail 4.0+ design); all panels are now FieldPanel (B10). |
| `a03-edit-standard-page` | [2.7](2.7/a03-edit-standard-page.png) | [2.15](2.15/a03-edit-standard-page.png) | [7.4](7.4/a03-edit-standard-page.png) | new admin UI |  |
| `a04-edit-event-index-page` | [2.7](2.7/a04-edit-event-index-page.png) | [2.15](2.15/a04-edit-event-index-page.png) | [7.4](7.4/a04-edit-event-index-page.png) | new admin UI |  |
| `a05-edit-event-page` | [2.7](2.7/a05-edit-event-page.png) | [2.15](2.15/a05-edit-event-page.png) | [7.4](7.4/a05-edit-event-page.png) | new admin UI | SnippetChooserPanel / ImageChooserPanel are now FieldPanel (B10); new StreamField UI. |
| `a06-edit-staff-index-page` | [2.7](2.7/a06-edit-staff-index-page.png) | [2.15](2.15/a06-edit-staff-index-page.png) | [7.4](7.4/a06-edit-staff-index-page.png) | new admin UI |  |
| `a07-edit-staff-page` | [2.7](2.7/a07-edit-staff-page.png) | [2.15](2.15/a07-edit-staff-page.png) | [7.4](7.4/a07-edit-staff-page.png) | new admin UI |  |
| `a08-edit-form-page` | [2.7](2.7/a08-edit-form-page.png) | [2.15](2.15/a08-edit-form-page.png) | [7.4](7.4/a08-edit-form-page.png) | new admin UI |  |
| `a09-edit-contact-page` | [2.7](2.7/a09-edit-contact-page.png) | [2.15](2.15/a09-edit-contact-page.png) | [7.4](7.4/a09-edit-contact-page.png) | new admin UI |  |
| `a10-modeladmin-events` | [2.7](2.7/a10-modeladmin-events.png) | [2.15](2.15/a10-modeladmin-events.png) | [7.4](7.4/a10-modeladmin-events.png) | new admin UI | ModelAdmin replaced by PageListingViewSet (B07), ordered by start date. |
| `a11-modeladmin-staff` | [2.7](2.7/a11-modeladmin-staff.png) | [2.15](2.15/a11-modeladmin-staff.png) | [7.4](7.4/a11-modeladmin-staff.png) | new admin UI | ModelAdmin replaced by PageListingViewSet (B07), ordered by department. |
| `a12-forms-index` | [2.7](2.7/a12-forms-index.png) | [2.15](2.15/a12-forms-index.png) | [7.4](7.4/a12-forms-index.png) | new admin UI |  |
| `a13-submissions-enquiry` | [2.7](2.7/a13-submissions-enquiry.png) | [2.15](2.15/a13-submissions-enquiry.png) | [7.4](7.4/a13-submissions-enquiry.png) | new admin UI | All 30 submissions with every value; same CSV export as 2.7 (via ?export=csv, B05). |
| `a14-submissions-contact` | [2.7](2.7/a14-submissions-contact.png) | [2.15](2.15/a14-submissions-contact.png) | [7.4](7.4/a14-submissions-contact.png) | new admin UI |  |
| `a15-school-settings` | [2.7](2.7/a15-school-settings.png) | [2.15](2.15/a15-school-settings.png) | [7.4](7.4/a15-school-settings.png) | new admin UI | BaseSetting is now BaseSiteSetting (B11); same fields. |
| `a16-snippets` | [2.7](2.7/a16-snippets.png) | [2.15](2.15/a16-snippets.png) | [7.4](7.4/a16-snippets.png) | new admin UI |  |

Front end: **11 of 13 pages pixel-identical** between 2.7 and 7.4.
