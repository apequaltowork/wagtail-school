"""
Make requests through Django's test client from `manage.py shell`, i.e. the way a
production WSGI server behaves: no system checks run first.

    python manage.py shell -c "exec(open('tools/request_without_checks.py', encoding='utf-8').read())"
"""
from django.test import Client

client = Client(raise_request_exception=True)
for path in ['/', '/admissions/enrolment-enquiry/']:
    response = client.get(path)
    print(response.status_code, path)
