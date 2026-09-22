"""
Drop and recreate this stage's database (and empty media/), for clean-slate checks.

    python tools/recreate_db.py --yes

Uses the credentials in settings/local.py. The app role owns its database and
has CREATEDB, so no superuser is needed.
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolsite.settings.dev')

import django  # noqa: E402

django.setup()

import psycopg2  # noqa: E402
from django.conf import settings  # noqa: E402

if '--yes' not in sys.argv:
    sys.exit('Refusing to drop the database without --yes')

db = settings.DATABASES['default']
conn = psycopg2.connect(dbname='postgres', user=db['USER'], password=db['PASSWORD'],
                        host=db['HOST'], port=db['PORT'])
conn.autocommit = True
with conn.cursor() as cur:
    cur.execute('DROP DATABASE IF EXISTS "{}"'.format(db['NAME']))
    cur.execute('CREATE DATABASE "{}" ENCODING \'UTF8\''.format(db['NAME']))
conn.close()
print('Recreated database', db['NAME'])

if os.path.isdir(settings.MEDIA_ROOT):
    shutil.rmtree(settings.MEDIA_ROOT)
    print('Removed', settings.MEDIA_ROOT)
