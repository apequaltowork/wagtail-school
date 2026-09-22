"""
What the forms look like to a WSGI server that never ran system checks (clean_name still blank).

    python manage.py shell -c "exec(open('tools/forms_without_checks.py', encoding='utf-8').read())"
"""
import re

from django.contrib.auth import get_user_model
from django.test import Client

from forms.models import FormPage

page = FormPage.objects.get(slug='enrolment-enquiry')
client = Client()

html = client.get(page.url).content.decode('utf-8')
names = sorted(set(re.findall(r'name="([^"]*)"', html)) - {'csrfmiddlewaretoken', 'query'})
print('Front-end form field names:', names)
print('Form fields built by FormBuilder:', list(page.get_form(page=page, user=None).fields.keys()))

client.force_login(get_user_model().objects.get(username='admin'))
listing = client.get('/admin/forms/submissions/{}/'.format(page.pk)).content.decode('utf-8')
print('Admin listing contains a seeded parent email:', 'example.com' in listing)
for export in ('?action=CSV', '?export=csv'):
    response = client.get('/admin/forms/submissions/{}/{}'.format(page.pk, export))
    raw = b''.join(response.streaming_content) if response.streaming else response.content
    body = raw.decode('utf-8', 'replace')
    print('Export {:<12} -> {} {}'.format(export, response.status_code, response.get('Content-Type')))
    if 'csv' in response.get('Content-Type', ''):
        print('   ' + '\n   '.join(body.splitlines()[:3]))
