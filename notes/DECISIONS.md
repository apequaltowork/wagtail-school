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

## D05 — PYTHONUTF8=1 in bin/rec
Windows pipes stdout as cp1252, so Django's console email backend crashed on non-ASCII form answers (log 012). The fix belongs in the environment, not the code: bin/rec exports `PYTHONUTF8=1`. Run by hand on Windows, set the same variable.

## D06 — Embed block is defined but not seeded
`BaseStreamBlock` includes `embed` (EmbedBlock), as the brief asks. Seeding it would mean embedding a real third-party video and fetching oEmbed over the network at render time, which conflicts with "fictional, no downloads" and makes the page-text baseline depend on the network. It stays available in the editor.

## D07 — StreamFields render with `{{ page.body }}`
This is the 2.7 idiom, and it wraps each block in `<div class="block-<type>">`. The CSS targets those wrapper classes (`.block-quote blockquote`, `.block-table table` …), the way a 2019 site typically did, so any change to the wrapper markup in later Wagtail versions will show up in the screenshots.

## D08 — Seed file naming and resets
`seed_demo --reset` deletes the pages under Home, then images, documents, snippets, settings and submissions, in its own transaction. Wagtail's post_delete handlers remove the files on commit, then the rebuild runs in a second transaction. Submissions are created in a shuffled order (fixed seed 2019) so enquiry and contact submissions interleave, and submit_time is then assigned in pk order across the last 182 days.

## D09 — `data-baseline="dynamic"`
Listings whose content depends on today's date (upcoming and past events, the home page's next three events, the "already taken place" note) carry `data-baseline="dynamic"`. The page-text baseline strips those elements, so a later stage run on a different day still compares like with like.
