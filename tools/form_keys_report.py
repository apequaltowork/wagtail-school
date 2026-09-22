"""
Print each form field's label, stored clean_name, and whether that key appears in stored
submission data. Run with `manage.py shell` so no system checks fire:

    python manage.py shell -c "exec(open('tools/form_keys_report.py', encoding='utf-8').read())"
"""
import json

from wagtail.contrib.forms.models import FormSubmission

from forms.models import ContactPage, FormPage

for page in list(FormPage.objects.all()) + list(ContactPage.objects.all()):
    stored = set()
    for submission in FormSubmission.objects.filter(page=page):
        stored.update(json.loads(submission.form_data).keys())
    print('== {} ({} submissions)'.format(page.slug, FormSubmission.objects.filter(page=page).count()))
    for field in page.form_fields.all():
        status = 'matches data' if field.clean_name in stored else 'NOT IN DATA'
        print('  {:<52} clean_name={!r:<48} {}'.format(field.label, field.clean_name, status))
