"""
Write notes/screenshots/compare.md: every 2.7 screenshot next to its 2.15 and 7.4 versions,
with a pixel comparison of 2.7 vs 7.4.

    python tools/compare_screenshots.py
"""
import os

from PIL import Image, ImageChops

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOTS = os.path.join(ROOT, 'notes', 'screenshots')

NOTES = {
    '09-enrolment-form.png': 'Identical after B21 (Django 4.0 widget markup); before the fix the options rendered bold.',
    '12-search-results.png': 'Expected difference (B18): the `database` search backend finds 7 results for "music" instead of 1.',
    '13-not-found.png': "Django's DEBUG 404 page on every stage (D20); only the debug page's own layout differs.",
    'a02-edit-home-page.png': 'New editor UI (Wagtail 4.0+ design); all panels are now FieldPanel (B10).',
    'a05-edit-event-page.png': 'SnippetChooserPanel / ImageChooserPanel are now FieldPanel (B10); new StreamField UI.',
    'a10-modeladmin-events.png': 'ModelAdmin replaced by PageListingViewSet (B07), ordered by start date.',
    'a11-modeladmin-staff.png': 'ModelAdmin replaced by PageListingViewSet (B07), ordered by department.',
    'a13-submissions-enquiry.png': 'All 30 submissions with every value; same CSV export as 2.7 (via ?export=csv, B05).',
    'a15-school-settings.png': 'BaseSetting is now BaseSiteSetting (B11); same fields.',
}


def verdict(a, b):
    x, y = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
    if x.size != y.size:
        return 'differs (size {}×{} → {}×{})'.format(*x.size, *y.size)
    box = ImageChops.difference(x, y).getbbox()
    return '**pixel-identical**' if box is None else 'differs in region {}'.format(box)


def main():
    names = sorted(os.listdir(os.path.join(SHOTS, '2.7')))
    lines = [
        '# Screenshots: 2.7 → 2.15 → 7.4',
        '',
        'Full-page screenshots at 1366px wide, taken by `tools/screenshots/shoot.js` on each stage.',
        'Front-end pages are compared pixel for pixel between 2.7 and 7.4. Admin screens differ by design',
        '(a new admin UI), so the notes say what changed.',
        '',
        '| Screen | 2.7 | 2.15 | 7.4 | 2.7 vs 7.4 | Notes |',
        '|---|---|---|---|---|---|',
    ]
    identical = front = 0
    for name in names:
        paths = {stage: os.path.join(SHOTS, stage, name) for stage in ('2.7', '2.15', '7.4')}
        links = ' | '.join(
            '[{0}]({0}/{1})'.format(stage, name) if os.path.exists(p) else '—'
            for stage, p in paths.items()
        )
        result = verdict(paths['2.7'], paths['7.4']) if os.path.exists(paths['7.4']) else 'missing'
        if not name.startswith('a'):
            front += 1
            identical += 'identical' in result
        elif result != '**pixel-identical**':
            result = 'new admin UI'
        lines.append('| `{}` | {} | {} | {} |'.format(name[:-4], links, result, NOTES.get(name, '')))
    lines += ['', 'Front end: **{} of {} pages pixel-identical** between 2.7 and 7.4.'.format(identical, front), '']
    with open(os.path.join(SHOTS, 'compare.md'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    print('\n'.join(lines[-2:]))


if __name__ == '__main__':
    main()
