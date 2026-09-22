# Project
- Demo Wagtail site for a fictional school (Kestrel Ridge College), built for a public upgrade video. All names, people and content are fictional. Never use real schools, real people's names, or photos of real people.
- The 2.7 codebase must stay period-accurate: Wagtail 2.7 / Django 2.2 APIs, written the way the 2.7 docs show (https://docs.wagtail.org/en/v2.7/).

# Environments — one folder, virtualenv and database per stage. Never modify an earlier stage.
| Stage | Folder | Virtualenv | Python | Database |
|---|---|---|---|---|
| 2.7  | D:\django\wagtail-school     | wagtail-school     | 3.8  | wagtail_school     |
| 2.15 | D:\django\wagtail-school-215 | wagtail-school-215 | 3.10 | wagtail_school_215 |
| 7.4  | D:\django\wagtail-school-74  | wagtail-school-74  | 3.12 | wagtail_school_74  |
- Machine: Windows 10. Shell for bin/rec is Git Bash. WORKON_HOME=D:\django\.virtualenvs.
- Pythons come from uv (`uv python install 3.8` / `3.10` / `3.12`); `uv python find <ver>` gives the path.
- Virtualenvs use virtualenvwrapper-win: `mkvirtualenv -p <python path> <name>`.
- Your shell does not keep activation between commands. Call binaries by full path, e.g.
  `bin/rec check "$WORKON_HOME/wagtail-school/Scripts/python.exe" manage.py check`
- PostgreSQL 16 runs natively (Windows service). Binaries: `C:\Program Files\PostgreSQL\16\bin` (psql, pg_dump, pg_restore).
  Postgres superuser admin (`psql -U postgres`) is done by the user, not by Claude — Claude prints the command, the user runs it.
  Ask the user once for the app DB user and password. Store them only in the gitignored settings/local.py.

# Requirements
- One requirements.txt for the life of the project. Never create another requirements file.
- When upgrading: packages that are deprecated or no longer needed stay in the file, commented out, with the reason and the version where they were dropped.

# Logging — the notes are the raw material for the video. Never skip them.
- bin/rec <slug> <command...> runs a command and saves its full output (stdout + stderr) to notes/logs/NNN-<slug>.log, where NNN auto-increments. Header: time, folder, command, git commit. Footer: exit code, duration. It prints the output too and returns the command's exit code.
- Use bin/rec for every install, check, makemigrations, migrate, test, seed, dump, restore, crawl — and anything that fails.
- notes/SESSION_LOG.md — after every step, append: time, what you did, why, log file, result.
- notes/SCENES.md — flag moments worth showing on camera: "[SCENE] <title> — log NNN / commit <sha> / screenshot <file> — why it matters" (errors, before/after, key decisions).
- notes/DECISIONS.md — every non-obvious choice and the reason.
- notes/UPGRADE_LOG.md (upgrade sessions only) — one entry per breakage:
    ID (B01, B02 …) · hop · symptom (exact error, first lines + log file) · cause (which Wagtail/Django version changed what) · fix (commit sha + the key before/after lines) · docs (versioned URL) · story value (High/Medium/Low)
- Git: commit after every logical step with a clear message, e.g. "build(events): add EventIndexPage and EventPage", "fix(2.15): replace SiteMiddleware". Never squash or rewrite history.
- Commits are authored as Ashish Pitroda <apequaltowork@gmail.com>. No AI attribution: no Co-Authored-By trailer, no "Generated with" lines. `.claude/` stays gitignored.
- Never write secrets (DB password, SECRET_KEY, admin password) into notes, logs or commits.

# Upgrade behaviour (later sessions)
- Order: bump requirements → install → run checks and migrations through bin/rec → let errors surface → fix each one, citing the versioned docs.
- Capture each failure before fixing it, even when the release notes already warned you about it. The video needs the real error on screen.
- Cite versioned docs only: https://docs.wagtail.org/en/v<version>/
