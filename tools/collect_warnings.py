"""
Collapse the warnings in one or more bin/rec logs into a de-duplicated list.

    python tools/collect_warnings.py <out.txt> <title line> <log> [<log> ...]
"""
import collections
import re
import sys

out_path, title, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
LOCATION = re.compile(r'(\S+\.py):(\d+): (\w*Warning): (.*)')

found = collections.OrderedDict()
for log in logs:
    lines = open(log, encoding='utf-8').read().splitlines()
    for i, line in enumerate(lines):
        match = LOCATION.search(line)
        if not match:
            continue
        path, lineno, kind, message = match.groups()
        path = path.replace('\\', '/')
        if 'site-packages/' in path:
            path = 'site-packages/' + path.split('site-packages/', 1)[1]
        else:
            path = re.sub(r'^.*?/wagtail-school[^/]*/', '', path)
        source = lines[i + 1].strip() if i + 1 < len(lines) else ''
        found.setdefault((kind, message), set()).add('{}:{}  |  {}'.format(path, lineno, source))

with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(title + '\n')
    f.write('Collected with python -Wa from: {}\n\n'.format(', '.join(logs)))
    for n, ((kind, message), where) in enumerate(found.items(), 1):
        f.write('{}. [{}] {}\n'.format(n, kind, message))
        for location in sorted(where):
            f.write('     {}\n'.format(location))
        f.write('\n')
print('{} distinct warnings -> {}'.format(len(found), out_path))
