"""
Record (or check) the upgrade baseline against a running server.

    python tools/baseline.py --base http://127.0.0.1:8027 --out baseline
    python tools/baseline.py --base http://127.0.0.1:8027 --out notes/check-2.15 --compare baseline

Writes:
    urls.txt                        "<status> <path>" for every live page plus extra routes
    page_text.json                  path -> normalised visible text of <main>
    counts.json                     pages per type, images, documents, snippets, submissions per form
    form_submissions_<slug>.csv     each form's submissions via the admin's own CSV export
    form_field_keys.json            per form: field label -> key stored in submission data

With --compare, also diffs the new files against an earlier baseline folder
and exits non-zero on any difference.

Needs DEMO_ADMIN_PASSWORD for the admin login. Dates-dependent markup marked
data-baseline="dynamic" is left out of page text.
"""
import argparse
import csv
import io
import json
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolsite.settings.dev')

import django  # noqa: E402

django.setup()

import requests  # noqa: E402
from bs4 import BeautifulSoup  # noqa: E402
from django.contrib.contenttypes.models import ContentType  # noqa: E402

try:
    from wagtail.models import Page  # Wagtail 3.0+
except ImportError:
    from wagtail.core.models import Page
from wagtail.contrib.forms.models import FormSubmission  # noqa: E402
try:
    from wagtail.documents import get_document_model  # Wagtail 2.8+
except ImportError:
    from wagtail.documents.models import get_document_model
from wagtail.images import get_image_model  # noqa: E402

from events.models import EventCategory  # noqa: E402
from forms.models import ContactPage, FormPage  # noqa: E402
from staff.models import Department  # noqa: E402

EXTRA_PATHS = [
    '/events/past/',
    '/events/?page=2',
    '/events/?category=sport',
    '/events/past/?category=academic',
    '/our-staff/?department=science',
    '/search/?query=music',
    '/search/?query=scholarship',
    '/search/',
    '/no-such-page/',
]


def form_pages():
    return list(FormPage.objects.live().order_by('path')) + list(ContactPage.objects.live().order_by('path'))


def normalise_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    main = soup.find(id='main-content') or soup.body or soup
    for tag in main.find_all(attrs={'data-baseline': 'dynamic'}):
        tag.decompose()
    for tag in main.find_all(['script', 'style', 'noscript']):
        tag.decompose()
    return ' '.join(main.get_text(' ').split())


def crawl(base, out):
    session = requests.Session()
    pages = Page.objects.live().filter(depth__gt=1).specific().order_by('path')
    paths = [page.url for page in pages]
    paths += EXTRA_PATHS
    paths += [document.url for document in get_document_model().objects.order_by('title')]

    statuses, texts = [], OrderedDict()
    for path in paths:
        response = session.get(base + path, allow_redirects=False, timeout=60)
        statuses.append('{} {}'.format(response.status_code, path))
        content_type = response.headers.get('Content-Type', '')
        if response.status_code == 200 and content_type.startswith('text/html'):
            texts[path] = normalise_text(response.text)
        print(response.status_code, path)

    with open(os.path.join(out, 'urls.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(statuses) + '\n')
    with open(os.path.join(out, 'page_text.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(texts, f, indent=2, ensure_ascii=False)
        f.write('\n')


def counts(out):
    per_type = OrderedDict()
    for page in Page.objects.filter(depth__gt=1).order_by('path'):
        ct = ContentType.objects.get_for_id(page.content_type_id)
        key = '{}.{}'.format(ct.app_label, ct.model)
        per_type[key] = per_type.get(key, 0) + 1
    data = OrderedDict([
        ('pages_total', Page.objects.filter(depth__gt=1).count()),
        ('pages_live', Page.objects.live().filter(depth__gt=1).count()),
        ('pages_by_type', OrderedDict(sorted(per_type.items()))),
        ('images', get_image_model().objects.count()),
        ('documents', get_document_model().objects.count()),
        ('snippets', OrderedDict([
            ('events.eventcategory', EventCategory.objects.count()),
            ('staff.department', Department.objects.count()),
        ])),
        ('form_submissions', OrderedDict(
            (page.slug, FormSubmission.objects.filter(page=page).count()) for page in form_pages()
        )),
    ])
    with open(os.path.join(out, 'counts.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2)
        f.write('\n')


def field_keys(out):
    data = OrderedDict()
    for page in form_pages():
        fields = OrderedDict((field.label, field.clean_name) for field in page.get_form_fields())
        stored = set()
        for submission in FormSubmission.objects.filter(page=page):
            stored.update(json.loads(submission.form_data).keys())
        data[page.slug] = OrderedDict([
            ('fields', fields),
            ('stored_keys', sorted(stored)),
            ('unmatched_labels', [label for label, key in fields.items() if key not in stored]),
        ])
    with open(os.path.join(out, 'form_field_keys.json'), 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def admin_session(base):
    password = os.environ.get('DEMO_ADMIN_PASSWORD')
    if not password:
        sys.exit('Set DEMO_ADMIN_PASSWORD to export form submissions')
    session = requests.Session()
    login_url = base + '/admin/login/'
    response = session.get(login_url)
    token = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', response.text).group(1)
    response = session.post(login_url, data={
        'csrfmiddlewaretoken': token, 'username': 'admin', 'password': password, 'next': '/admin/',
    }, headers={'Referer': login_url})
    if '/admin/login/' in response.url:
        sys.exit('Admin login failed')
    return session


def export_csv(base, out):
    session = admin_session(base)
    for page in form_pages():
        url = '{}/admin/forms/submissions/{}/?action=CSV'.format(base, page.pk)
        response = session.get(url)
        response.raise_for_status()
        path = os.path.join(out, 'form_submissions_{}.csv'.format(page.slug))
        with open(path, 'wb') as f:
            f.write(response.content)
        rows = list(csv.reader(io.StringIO(response.content.decode('utf-8'))))
        print('exported {} rows from {}'.format(len(rows) - 1, url))


def compare(out, reference):
    problems = 0
    for name in sorted(os.listdir(reference)):
        ref_path, new_path = os.path.join(reference, name), os.path.join(out, name)
        if name == 'pip-freeze.txt' or not os.path.isfile(ref_path):
            continue
        if not os.path.exists(new_path):
            print('MISSING', name)
            problems += 1
            continue
        with open(ref_path, encoding='utf-8') as a, open(new_path, encoding='utf-8') as b:
            if a.read() != b.read():
                print('DIFFERS', name)
                problems += 1
            else:
                print('same   ', name)
    return problems


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--base', default='http://127.0.0.1:8027')
    parser.add_argument('--out', default='baseline')
    parser.add_argument('--compare')
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)
    crawl(args.base.rstrip('/'), args.out)
    counts(args.out)
    field_keys(args.out)
    export_csv(args.base.rstrip('/'), args.out)
    if args.compare:
        sys.exit(1 if compare(args.out, args.compare) else 0)


if __name__ == '__main__':
    main()
