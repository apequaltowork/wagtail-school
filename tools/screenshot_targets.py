"""
Print the screenshot targets for this stage as JSON (used by tools/screenshots/shoot.js).
Resolves page and site IDs from the database so the same list works on every stage.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolsite.settings.dev')

import django  # noqa: E402

django.setup()

try:
    from wagtail.models import Page  # Wagtail 3.0+
except ImportError:
    from wagtail.core.models import Page


def page_id(url_path_suffix):
    return Page.objects.get(url_path='/home/' + url_path_suffix).pk


frontend = [
    ('01-home', '/'),
    ('02-standard-page', '/about/principals-welcome/'),
    ('03-fees', '/admissions/fees-and-scholarships/'),
    ('04-events-index', '/events/'),
    ('05-event-detail', '/events/spring-open-morning/'),
    ('06-past-events', '/events/past/'),
    ('07-staff-index', '/our-staff/'),
    ('08-staff-detail', '/our-staff/miriam-okonkwo-hale/'),
    ('09-enrolment-form', '/admissions/enrolment-enquiry/'),
    ('11-contact', '/contact-us/'),
    ('12-search-results', '/search/?query=music'),
    ('13-not-found', '/no-such-page/'),
]

editors = [
    ('home-page', ''),
    ('standard-page', 'about/principals-welcome/'),
    ('event-index-page', 'events/'),
    ('event-page', 'events/spring-open-morning/'),
    ('staff-index-page', 'our-staff/'),
    ('staff-page', 'our-staff/miriam-okonkwo-hale/'),
    ('form-page', 'admissions/enrolment-enquiry/'),
    ('contact-page', 'contact-us/'),
]

admin = [('a01-dashboard', '/admin/')]
for i, (name, suffix) in enumerate(editors, 2):
    admin.append(('a{:02d}-edit-{}'.format(i, name), '/admin/pages/{}/edit/'.format(page_id(suffix))))
admin += [
    ('a10-modeladmin-events', '/admin/events/eventpage/'),
    ('a11-modeladmin-staff', '/admin/staff/staffpage/'),
    ('a12-forms-index', '/admin/forms/'),
    ('a13-submissions-enquiry', '/admin/forms/submissions/{}/'.format(page_id('admissions/enrolment-enquiry/'))),
    ('a14-submissions-contact', '/admin/forms/submissions/{}/'.format(page_id('contact-us/'))),
    ('a15-school-settings', '/admin/settings/core/schoolsettings/'),
    ('a16-snippets', '/admin/snippets/'),
]

print(json.dumps({
    'frontend': frontend,
    'admin': admin,
    'form': {'name': '10-form-thank-you', 'path': '/admissions/enrolment-enquiry/'},
}))
