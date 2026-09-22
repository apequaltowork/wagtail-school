"""
Recover logged search queries lost in the 2.15 -> 7.4 jump (UPGRADE_LOG B16).

Wagtail 6.0 turned wagtailsearchpromotions.0004_copy_queries into a no-op; the real copy
only ran on Wagtail 5.x. A project that jumps straight from 2.x to 6.0+ therefore gets
wagtailsearch.0008 (drop Query / QueryDailyHits) without the copy. This reads the old
rows from the pre-upgrade pg_dump and recreates them with the search_promotions models.

    python tools/recover_search_queries.py ../wagtail-school-215/dumps/wagtail_school_215.dump
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'schoolsite.settings.dev')

import django  # noqa: E402

django.setup()

from django.db import transaction  # noqa: E402
from wagtail.contrib.search_promotions.models import Query, QueryDailyHits  # noqa: E402

PG_BIN = os.environ.get('PG_BIN', r'C:\Program Files\PostgreSQL\16\bin')


def copy_rows(dump, table):
    """Return the rows of `table` from a custom-format dump, as lists of strings."""
    sql = subprocess.check_output(
        [os.path.join(PG_BIN, 'pg_restore'), '--data-only', '-t', table, '-f', '-', dump]
    ).decode('utf-8')
    rows, inside = [], False
    for line in sql.splitlines():
        if line.startswith('COPY public.{} '.format(table)):
            inside = True
            continue
        if inside:
            if line == '\\.':
                break
            rows.append(line.split('\t'))
    return rows


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: python tools/recover_search_queries.py <pre-upgrade dump>')
    dump = sys.argv[1]

    queries = copy_rows(dump, 'wagtailsearch_query')          # id, query_string
    hits = copy_rows(dump, 'wagtailsearch_querydailyhits')    # id, date, hits, query_id
    print('found {} queries and {} daily-hit rows in {}'.format(len(queries), len(hits), dump))

    with transaction.atomic():
        by_old_id = {}
        for old_id, query_string in queries:
            query, created = Query.objects.get_or_create(query_string=query_string)
            by_old_id[old_id] = query
            print('  query {!r}: {}'.format(query_string, 'created' if created else 'already present'))
        for _id, date, count, old_query_id in hits:
            row, created = QueryDailyHits.objects.get_or_create(
                query=by_old_id[old_query_id], date=date, defaults={'hits': int(count)},
            )
            if not created and row.hits < int(count):
                row.hits = int(count)
                row.save()
            print('  hits {} on {} for {!r}'.format(row.hits, date, row.query.query_string))

    print('now: {} queries, {} daily-hit rows'.format(Query.objects.count(), QueryDailyHits.objects.count()))


if __name__ == '__main__':
    main()
