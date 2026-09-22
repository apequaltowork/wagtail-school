"""
pg_dump -Fc this stage's database using the credentials from settings/local.py.

    python tools/dump_db.py dumps/wagtail_school_27.dump

The password is passed to pg_dump through PGPASSWORD, so it never appears in
the command line or in bin/rec logs.
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolsite.settings.dev')

import django  # noqa: E402

django.setup()

from django.conf import settings  # noqa: E402

PG_BIN = os.environ.get('PG_BIN', r'C:\Program Files\PostgreSQL\16\bin')

if len(sys.argv) != 2:
    sys.exit('usage: python tools/dump_db.py <output.dump>')

db = settings.DATABASES['default']
out = sys.argv[1]
os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
env = dict(os.environ, PGPASSWORD=db['PASSWORD'])
cmd = [os.path.join(PG_BIN, 'pg_dump'), '-Fc', '--no-owner', '-h', db['HOST'], '-p', str(db['PORT']),
       '-U', db['USER'], '-f', out, db['NAME']]
print('pg_dump -Fc', db['NAME'], '->', out)
subprocess.check_call(cmd, env=env)
print('wrote {} ({:,} bytes)'.format(out, os.path.getsize(out)))
