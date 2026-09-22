"""How I Prompted an AI to Upgrade a Wagtail Site.

Scene spec for video/build.py. The companion to video/upgrade/: that one is about what broke,
this one is about the method -- the three prompts I gave Claude (Claude Code), why each part is
there, where it needed me, and the mistakes it made that the method caught.

Quoted prompt lines are verbatim from the brief. Numbers come from the repo (git log, notes/).
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402

BADGE = 'WAGTAIL <b>UPGRADE</b> &nbsp;&middot;&nbsp; how I prompted it'

CSS = """
<style>
.big-num { font-size: 132px; font-weight: 800; line-height: 1; letter-spacing: -4px; }
.big-num.teal { color: var(--teal); }
.big-num.red { color: var(--red); }
.stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 50px; margin-top: 10px; }
.stat-grid .cap { font-size: 30px; color: var(--muted); margin-top: 10px; }
.prompt { background: #1a1f2e; border-left: 8px solid var(--amber); border-radius: 12px;
          padding: 36px 44px; font-family: var(--mono); font-size: 33px; line-height: 1.5;
          color: var(--fg); white-space: pre-wrap; }
.prompt .who { display: block; font-family: var(--sans); font-size: 24px; letter-spacing: 4px;
               text-transform: uppercase; color: var(--amber); margin-bottom: 18px; font-weight: 600; }
.why { font-size: 38px; color: var(--muted); line-height: 1.4; margin-top: 40px; max-width: 1550px; }
.why b { color: var(--fg); }
.num { display: inline-block; font-size: 30px; color: var(--bg); background: var(--teal);
       border-radius: 10px; padding: 4px 16px; margin-right: 18px; font-weight: 700; }
table.small { font-size: 31px; }
table.small td, table.small th { padding: 16px 22px; }
.caught { color: var(--teal); }
.slip { color: var(--red); }
</style>
"""


def principle(n: int, title: str, quote: str, why: str, say: str, sid: str) -> Scene:
    return Scene(
        id=sid,
        body=CSS + f"""
        <div class="eyebrow"><span class="num">{n}</span>{title}</div>
        <div class="prompt"><span class="who">From my prompt</span>{quote}</div>
        <div class="why">{why}</div>
        """,
        say=say,
    )


EPISODE = Episode(
    key="claude-workflow",
    title="How I Prompted an AI to Upgrade a Wagtail Site",
    badge=BADGE,
    intro_say="How I prompted an AI to upgrade a Wagtail site, from two point seven to seven point four.",
    outro_say="The prompts, the rules file and every log are in the repo. Thanks for watching.",
    scenes=[
        Scene(
            id="hook",
            body=CSS + """
            <div class="eyebrow">What came out of three prompts</div>
            <div class="stat-grid">
              <div><div class="big-num teal">62</div><div class="cap">commits, one per step</div></div>
              <div><div class="big-num">133</div><div class="cap">recorded command logs</div></div>
              <div><div class="big-num red">22</div><div class="cap">breakages, each written up</div></div>
              <div><div class="big-num">29</div><div class="cap">decisions, with reasons</div></div>
            </div>
            <div class="sub" style="margin-top:70px">Plus a blog post and a video. The AI did the typing.
            The prompts decided whether any of it could be trusted.</div>
            """,
            say="I gave an AI, Claude, three prompts. It built a twenty nineteen Wagtail site, upgraded it "
                "twice, and recorded everything. Sixty two commits, a hundred and thirty three command logs, "
                "twenty two breakages, twenty nine written decisions. The AI did the typing. The prompts "
                "decided whether any of it could be trusted. This video is about those prompts.",
        ),
        Scene(
            id="three_prompts",
            body=CSS + """
            <div class="eyebrow">Three prompts, run in order</div>
            <table class="small">
              <tr><th>Prompt</th><th>Job</th><th>Ends with tag</th></tr>
              <tr><td class="k">1</td><td class="v">Build a period-accurate Wagtail 2.7 site + baseline</td><td class="v">v2.7-baseline</td></tr>
              <tr><td class="k">2</td><td class="v">Upgrade 2.7 &rarr; 2.15 LTS</td><td class="v">v2.15</td></tr>
              <tr><td class="k">3</td><td class="v">Upgrade 2.15 &rarr; 7.4 LTS in one jump</td><td class="v">v7.4</td></tr>
            </table>
            <div class="why">Each stage gets its <b>own folder, virtualenv and database</b>. Nothing
            downstream can damage what came before.</div>
            """,
            say="Three prompts, run in order. One builds the old site and records a baseline. One upgrades "
                "to two fifteen. One jumps to seven point four. Each stage gets its own folder, its own "
                "virtual environment and its own database, so nothing later can damage what came before.",
        ),

        # ------------------------------------------------------------ the method
        Scene(
            id="method_title",
            classes="title-slide",
            body="""
            <div class="eyebrow">Part one</div>
            <h1>The prompt method</h1>
            <div class="rule"></div>
            <div class="sub">Eight things in the prompts that did the real work.</div>
            """,
            say="Part one. Eight things in those prompts that did the real work.",
        ),
        principle(
            1, "Plan first, then wait",
            "STEP 0 — PLAN FIRST\nBefore writing any code, show me a short plan ...\nWait for my approval.",
            "Every prompt started with a plan I could reject. That's where I <b>changed the folder name</b>, "
            "picked how Postgres gets installed, and chose between upgrade paths.",
            "One. Plan first, then wait. Every prompt opened by asking for a plan and stopping. That plan "
            "is the cheapest place to correct it. It is where I renamed the project folder, chose how "
            "Postgres gets installed, and picked between the upgrade paths the docs allow.",
            "p1_plan",
        ),
        principle(
            2, "Put the rules in a file, not in the chat",
            "In it, create CLAUDE.md with the rules below.\nThey apply to this session and to the\nlater upgrade sessions.",
            "Stages, logging, commits, secrets, how to upgrade. <b>Written once</b>, read at the start of "
            "every later prompt &mdash; the second and third prompts just say &ldquo;read CLAUDE.md and follow it&rdquo;.",
            "Two. Put the rules in a file, not in the chat. The first prompt told it to write a rules file "
            "into the project. Which folder is which stage, how to log, how to commit, never to write "
            "secrets. The later prompts just say, read that file and follow it. The rules survive between "
            "sessions because they live in the repo.",
            "p2_rules",
        ),
        Scene(
            id="p3_rec",
            body=CSS + """
            <div class="eyebrow"><span class="num">3</span>Record every command</div>
            <div class="prompt"><span class="who">From my prompt</span>Use bin/rec for every install, check, makemigrations,
migrate, test, seed, dump, restore, crawl — and anything that fails.</div>
            <pre class="code" style="font-size:25px;margin-top:30px"><span class="c"># rec 045-request-no-checks-1
# time:    2026-09-22 10:39:50 +0530
# folder:  /d/django/wagtail-school-215
# command: ... manage.py shell -c exec(open('tools/request_without_checks.py' ...
# commit:  722c6f4</span>
<span class="bad">ModuleNotFoundError: No module named 'wagtail.core.middleware'</span>
<span class="c"># exit code: 1</span></pre>
            """,
            say="Three. Record every command. A tiny script wraps every command and saves the full output, "
                "with the time, the folder and the git commit. That gave me a hundred and thirty three logs. "
                "They are the proof behind every claim in the blog and the other video, and the only reason "
                "those videos can show real errors instead of recreated ones.",
        ),
        principle(
            4, "Capture the failure before fixing it",
            "Capture each failure before fixing it, even when the\nrelease notes already warned you about it.\nThe video needs the real error on screen.",
            "An AI that has read the release notes will happily <b>pre-fix</b> everything. This line forced "
            "it to let each error happen first &mdash; which is how the silent problems were found.",
            "Four. Capture the failure before fixing it. An AI that has read the release notes will "
            "happily fix things before they break, and you learn nothing. This line made it let every "
            "error happen first. That is exactly how the silent problems surfaced, the ones no release "
            "note warned about.",
            "p4_capture",
        ),
        principle(
            5, "Define done as things a machine can check",
            "DONE WHEN\n- check is clean, makemigrations --check reports no changes\n- seed_demo --reset runs twice from an empty database\n- Every page type renders with status 200 ...",
            "Plus a <b>baseline</b>: every URL, the text of every page, the form CSV exports, screenshots. "
            "Each upgrade had to match it &mdash; byte for byte, pixel for pixel.",
            "Five. Define done as things a machine can check. Not, it works. Checks clean. Migrations "
            "clean. Seeds twice from an empty database. Every page returns two hundred. And a baseline, "
            "every U R L, the text of every page, the form exports and screenshots, that each upgrade had "
            "to match byte for byte.",
            "p5_done",
        ),
        principle(
            6, "Make the test data realistic, and plant the traps",
            "use these exact labels. They deliberately include\napostrophes, a slash, a question mark and accented\ncharacters, because form-field naming changes\nduring the upgrade.",
            "And: submissions created through <b>Wagtail's own code path</b>, never hand-written JSON. "
            "That's the only reason the biggest data problem showed up at all.",
            "Six. Make the test data realistic, and plant the traps. The form labels were chosen to break "
            "the form field naming change, and the submissions had to be created through Wagtail's own "
            "code, never hand written. Without that, the biggest data problem of the whole upgrade would "
            "never have appeared.",
            "p6_data",
        ),
        principle(
            7, "Pin the period, forbid the shortcuts",
            "Write normal, clean 2019 code — no planted bugs,\nno deliberately odd code, and no future-proofing\n(no newer import paths, no JSON StreamField).",
            "Left alone, an AI writes <b>today's</b> code. Then there's nothing to upgrade. The prompt listed "
            "the exact 2.7 idioms to use.",
            "Seven. Pin the period, and forbid the shortcuts. Left alone, an AI writes today's code, and "
            "then there is nothing to upgrade. The prompt listed the exact twenty nineteen idioms to use, "
            "and banned future proofing.",
            "p7_period",
        ),
        principle(
            8, "Say how to choose, and demand sources",
            "Where the docs offer more than one path, follow the\ndocs' recommended path, choose the smallest change for\nthis hop, and note the alternative in DECISIONS.md.\n\nCite versioned docs only.",
            "Every fix in the upgrade log links the <b>versioned</b> release note it came from. Every choice "
            "records the road not taken.",
            "Eight. Say how to choose, and demand sources. When there were two ways to fix something, the "
            "prompt said which one to prefer and to write down the other. And every fix had to cite the "
            "release notes for that exact version.",
            "p8_choose",
        ),

        # ------------------------------------------------------------ where it needed me
        Scene(
            id="me_title",
            classes="title-slide",
            body="""
            <div class="eyebrow">Part two</div>
            <h1>Where it needed me</h1>
            <div class="rule"></div>
            """,
            say="Part two. Where it needed me.",
        ),
        Scene(
            id="decisions",
            body=CSS + """
            <div class="eyebrow">It stopped and asked &mdash; the calls were mine</div>
            <table class="small">
              <tr><td class="k">Project folder name</td><td class="v">renamed to <b>wagtail-school</b></td></tr>
              <tr><td class="k">PostgreSQL</td><td class="v">native install, not Docker</td></tr>
              <tr><td class="k">Commit authorship</td><td class="v">mine, no AI attribution lines</td></tr>
              <tr><td class="k">SiteMiddleware</td><td class="v">replace it, don't use the legacy path</td></tr>
              <tr><td class="k">ModelAdmin</td><td class="v">PageListingViewSet, not the external package</td></tr>
              <tr><td class="k">Search query logging</td><td class="v">keep it via search_promotions</td></tr>
            </table>
            """,
            say="It stopped and asked whenever there was a real choice. The folder name. Docker or a native "
                "Postgres. Whose name goes on the commits. And for the upgrade itself, which replacement to "
                "use for site middleware, for model admin, and whether to keep search logging. Each time it "
                "gave a recommendation and the trade off. The call was mine.",
        ),
        Scene(
            id="windows",
            body=CSS + """
            <div class="eyebrow">The brief was written for Linux</div>
            <div class="cols">
              <div class="col"><h3>My prompt said</h3>
                <p><b>~/Desktop/django</b></p><p><b>sudo -u postgres</b></p><p><b>mkvirtualenv</b>, bin/ paths</p></div>
              <div class="col hero"><h3>My machine is Windows</h3>
                <p>D:\\django, a native PostgreSQL service</p><p>virtualenvwrapper-win, Scripts\\ paths</p>
                <p>Every adaptation written down as a decision</p></div>
            </div>
            """,
            say="My prompts were written for Linux. Desktop paths, sudo, bin folders. My machine runs Windows. "
                "It adapted all of it, told me before it started, and wrote each adaptation down as a decision, "
                "so the later sessions knew too.",
        ),
        Scene(
            id="passwords",
            body=CSS + """
            <div class="eyebrow">What it wouldn't do</div>
            <div class="quote">It won't type your database superuser password. <span class="hl">It hands you
            the command</span> &mdash; and when pasting didn't work for me, a file I could double-click.</div>
            """,
            say="And some things it will not do. It would not type my database superuser password. It gave me "
                "the command to run myself. When pasting that into a terminal did not work for me, it wrote a "
                "small file I could just double click. The secret never passed through the AI.",
        ),

        # ------------------------------------------------------------ mistakes
        Scene(
            id="mistakes_title",
            classes="title-slide",
            body="""
            <div class="eyebrow">Part three</div>
            <h1>It made mistakes</h1>
            <div class="rule"></div>
            <div class="sub">The method caught every one of them.</div>
            """,
            say="Part three. It made mistakes. Here are the real ones, and what caught each of them.",
        ),
        Scene(
            id="mistakes_table",
            body=CSS + """
            <table class="small">
              <tr><th>The slip</th><th>What caught it</th></tr>
              <tr><td class="slip">.gitignore <b>static/</b> also hid the app's own CSS</td><td class="caught">reviewing the first commit's file list</td></tr>
              <tr><td class="slip">Search page crashed with a 500</td><td class="caught">the baseline crawler</td></tr>
              <tr><td class="slip">Event card images stretched</td><td class="caught">screenshot review</td></tr>
              <tr><td class="slip">Dropped Unidecode &mdash; the seed still imported it</td><td class="caught">seeding a fresh database</td></tr>
              <tr><td class="slip">Placeholder commit hashes in the upgrade log</td><td class="caught">checking against git log</td></tr>
              <tr><td class="slip">&ldquo;18 loud errors&rdquo; in the other video's hook</td><td class="caught">checking claims against the data</td></tr>
            </table>
            """,
            say="Its ignore file hid the site's own style sheets. The search page it built crashed. The event "
                "card images were stretched. During the upgrade it removed a package that its own seed script "
                "still imported. It drafted the upgrade log with commit hashes that did not exist yet. And in "
                "the other video's opening, it claimed eighteen loud errors, which the data did not support.",
        ),
        Scene(
            id="mistakes_lesson",
            body=CSS + """
            <div class="quote">Not one of these was caught by the AI <span class="hl">&ldquo;being careful&rdquo;</span>.
            Each was caught by a check the prompt required.</div>
            """,
            say="Not one of those was caught by the AI simply being careful. Each one was caught by a check the "
                "prompt required. A crawl, a screenshot, a fresh database, a comparison against the data. That "
                "is the whole point of writing done as things a machine can check.",
        ),

        # ------------------------------------------------------------ takeaways
        Scene(
            id="result",
            body=CSS + """
            <div class="eyebrow">What the method produced</div>
            <ul class="bullets">
              <li>11 of 13 pages <b>pixel-identical</b> across seven years of Wagtail</li>
              <li>Form exports <b>byte-for-byte</b> identical, every submission present</li>
              <li>Two silent data problems found and fixed</li>
              <li>A history you can replay one commit at a time</li>
            </ul>
            """,
            say="And the result. Eleven of thirteen pages pixel identical across seven years of Wagtail. Form "
                "exports byte for byte identical. Two silent data problems found and fixed. And a history you "
                "can replay one commit at a time.",
        ),
        Scene(
            id="checklist",
            body=CSS + """
            <div class="eyebrow">Put these in your own prompt</div>
            <ul class="bullets" style="font-size:40px">
              <li style="font-size:40px;margin-bottom:26px">Plan first, then wait for approval</li>
              <li style="font-size:40px;margin-bottom:26px">A rules file in the repo, read every session</li>
              <li style="font-size:40px;margin-bottom:26px">Log every command; capture failures before fixing</li>
              <li style="font-size:40px;margin-bottom:26px">&ldquo;Done&rdquo; = checks a machine can run, against a baseline</li>
              <li style="font-size:40px;margin-bottom:26px">Realistic data with deliberate traps</li>
              <li style="font-size:40px;margin-bottom:26px">How to choose between fixes &mdash; and cite versioned docs</li>
            </ul>
            """,
            say="So, if you write your own prompt for this. Plan first, and wait. A rules file in the repo. Log "
                "every command and capture failures before fixing them. Define done as checks a machine can "
                "run against a baseline. Use realistic data with deliberate traps. And say how to choose "
                "between fixes, with versioned sources.",
        ),
        Scene(
            id="repo",
            body="""
            <div class="eyebrow">Everything is in the repo</div>
            <h2>github.com/apequaltowork/wagtail-school</h2>
            <ul class="bullets">
              <li><b>CLAUDE.md</b> &mdash; the rules file</li>
              <li><b>notes/</b> &mdash; session log, decisions, upgrade log, 133 command logs</li>
              <li>The other video: <b>everything that broke</b></li>
            </ul>
            """,
            say="Everything is in the repo. The rules file, the session log, the decisions, the upgrade log and "
                "all the command logs. And if you want the breakages themselves, watch the other video, "
                "everything that broke.",
        ),
    ],
)
