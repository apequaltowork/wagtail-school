# Decisions

Every non-obvious choice, and why.

## D01 — Windows adaptations of the brief
The brief was written for Linux/Mac (`~/Desktop/django`, `sudo -u postgres`, POSIX virtualenvwrapper). This machine is Windows 10, so:
- Project root is `D:\django\wagtail-school` (renamed from `wagtail-school-demo` at the owner's request). Virtualenv and database names follow: `wagtail-school` / `wagtail_school`, and later `-215` / `-74`.
- Python 3.8 comes from `uv python install 3.8` (only 3.12 was installed). The virtualenv is made with virtualenvwrapper-win (`mkvirtualenv -p`), and binaries live under `Scripts\` rather than `bin/`.
- PostgreSQL 16 is a native Windows install. Superuser admin work (`psql -U postgres`) is run by the owner, which replaces `sudo -u postgres`. The app role owns its database and has CREATEDB so the Django test runner works.
- `bin/rec` is a bash script run under Git Bash. `.gitattributes` keeps it LF.

## D02 — School name
A web search for "Kestrel Ridge College" found no school by that name. The closest hit was a US communications consultancy, "Kestrel Ridge Education & Communication Developers", which is not a school. The name is kept, with a fictional suburb, "Kestrel Ridge, NSW", and a fictional founding year, 1962.

## D03 — Commit authorship
Commits are authored by the channel owner, with no AI attribution trailers. The repo history is part of the public video.

## D04 — `static/` in .gitignore
The brief says to ignore collected static output. `wagtail start` keeps source static files in `schoolsite/static/`, and `collectstatic` writes to `<root>/static/`. So only the root `/static/` is ignored (anchored), and `schoolsite/static/` (Bootstrap, CSS, fonts) is committed.
