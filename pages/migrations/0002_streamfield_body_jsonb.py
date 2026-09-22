# Hand-written for the 2.15 -> 7.4 jump (UPGRADE_LOG B15).
#
# Wagtail 3.0-5.x generated an AlterField (use_json_field=True) that converted
# StreamField columns from text to jsonb. From Wagtail 6.0, use_json_field is
# ignored and no longer deconstructed, so a project that skips 3.0-5.x never gets
# that migration: makemigrations sees no change and the column silently stays text.
# This converts the column in place; on a database created by Wagtail 6.0+ the
# column is already jsonb and the ALTER is a no-op. Model state is unchanged.
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL(
            sql='ALTER TABLE pages_standardpage ALTER COLUMN body TYPE jsonb USING body::jsonb',
            reverse_sql='ALTER TABLE pages_standardpage ALTER COLUMN body TYPE text USING body::text',
        ),
    ]
