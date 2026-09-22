"""I Upgraded Wagtail 2.7 -> 7.4 -- Everything That Broke.

Scene spec for video/build.py. The script follows blog/wagtail-2.7-to-7.4-everything-that-broke.md.

Every terminal output below is pasted from the recorded logs in notes/logs/ (log numbers in
the comments). Long lines are shortened with an ellipsis, never reworded. Commands are shown
as plain `python manage.py ...` -- in the recordings they ran through bin/rec with the full
virtualenv path. The B04 ">>>" lines name what tools/forms_without_checks.py checked (logs 048,
055); their outputs are that script's real output.
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
VIDEO = HERE.parent
REPO = VIDEO.parent
sys.path.insert(0, str(VIDEO))
from build import Episode, Scene  # noqa: E402
from term import Cmd, terminal_scene  # noqa: E402

BADGE = 'WAGTAIL <b>2.7 &rarr; 7.4</b> &nbsp;&middot;&nbsp; everything that broke'
P27 = "(2.7) &gt;"
P215 = "(2.15) &gt;"
P74 = "(7.4) &gt;"
PY = "&gt;&gt;&gt;"

SHOTS = REPO / "notes" / "screenshots"
BLOG_IMG = REPO / "blog" / "images"

CSS = """
<style>
.shot { border: 2px solid var(--line); border-radius: 14px; overflow: hidden;
        box-shadow: 0 30px 70px rgba(0,0,0,.45); background: #fff; }
.shot img { display: block; width: 100%; }
.shot.crop img { object-fit: cover; object-position: top; }
.shotbar { background: #161925; padding: 12px 22px; font-family: var(--mono);
           font-size: 24px; color: var(--muted); border-bottom: 2px solid var(--line); }
.pair { display: flex; gap: 36px; align-items: flex-start; }
.pair > div { flex: 1; }
.lbl { font-size: 28px; letter-spacing: 4px; text-transform: uppercase; color: var(--teal);
       margin-bottom: 14px; font-weight: 600; }
.lbl.bad { color: var(--red); }
.big-num { font-size: 150px; font-weight: 800; line-height: 1; letter-spacing: -5px; }
.big-num.red { color: var(--red); }
.big-num.teal { color: var(--teal); }
.stat-row { display: flex; gap: 90px; align-items: flex-end; margin-top: 20px; }
.stat-row .cap { font-size: 30px; color: var(--muted); margin-top: 10px; }
table.small { font-size: 30px; }
table.small td, table.small th { padding: 16px 22px; }
td.err { color: var(--red); font-family: var(--mono); font-size: 26px; }
td.fix { color: var(--teal); font-family: var(--mono); font-size: 26px; }
.flow { display: flex; align-items: center; gap: 40px; font-size: 64px; font-weight: 700; }
.flow .v { border: 3px solid var(--teal); border-radius: 22px; padding: 30px 46px; }
.flow .v small { display: block; font-size: 26px; font-weight: 500; color: var(--muted); margin-top: 8px; }
.flow .arr { color: var(--teal); }
</style>
"""


def img(path: Path, width: str = "100%", height: str = "", label: str = "", crop: bool = False) -> str:
    style = f"width:{width}"
    img_style = f' style="height:{height}"' if height else ""
    bar = f'<div class="shotbar">{label}</div>' if label else ""
    cls = "shot crop" if crop else "shot"
    return f'<div class="{cls}" style="{style}">{bar}<img src="{path.as_uri()}"{img_style} alt=""></div>'


EPISODE = Episode(
    key="upgrade",
    title="I Upgraded Wagtail 2.7 to 7.4 - Everything That Broke",
    badge=BADGE,
    intro_say="I upgraded a Wagtail two point seven site to Wagtail seven point four. "
              "Here is everything that broke.",
    outro_say="The code, every log and every screenshot are on GitHub. Thanks for watching.",
    scenes=[
        # ------------------------------------------------------------------ hook
        Scene(
            id="hook",
            body=CSS + """
            <div class="eyebrow">Seven years of Wagtail, one upgrade</div>
            <div class="stat-row">
              <div><div class="big-num red">22</div><div class="cap">things broke</div></div>
              <div><div class="big-num teal">4</div><div class="cap">broke silently</div></div>
            </div>
            <div class="sub" style="margin-top:70px">Wagtail 2.7 &rarr; 7.4 &nbsp;&middot;&nbsp;
            Django 2.2 &rarr; 5.2 &nbsp;&middot;&nbsp; Python 3.8 &rarr; 3.12</div>
            """,
            say="Twenty two things broke. Most of them were loud errors that take a minute each "
                "to fix. Four of them broke silently. Green checks, working pages, and quietly lost "
                "data. Those four are what this video is really about.",
        ),

        # ------------------------------------------------------------------ the site
        Scene(
            id="the_site",
            body=CSS + f"""
            <div class="pair">
              <div style="flex:1.25">{img(SHOTS / '2.7' / '01-home.png', height='640px', crop=True,
                                          label='Kestrel Ridge College &middot; Wagtail 2.7')}</div>
              <div>
                <div class="eyebrow">The test subject</div>
                <ul class="bullets" style="font-size:36px">
                  <li style="font-size:36px;margin-bottom:26px">A fictional K&ndash;12 school, built on Wagtail 2.7</li>
                  <li style="font-size:36px;margin-bottom:26px">43 pages, StreamField everywhere</li>
                  <li style="font-size:36px;margin-bottom:26px">Events, staff, snippets, settings</li>
                  <li style="font-size:36px;margin-bottom:26px">Two forms, 40 real submissions</li>
                </ul>
              </div>
            </div>
            """,
            say="The test subject is a school website. Kestrel Ridge College. It is fictional, but it "
                "is built like a real one. Forty three pages, StreamField everywhere, events, staff "
                "profiles, snippets, site settings, and two forms with forty real submissions.",
        ),
        Scene(
            id="period_code",
            body="""
            <div class="eyebrow">Written the way 2019 wrote it</div>
            <pre class="code" style="font-size:31px"><span class="k">from</span> wagtail.core.fields <span class="k">import</span> StreamField
<span class="k">from</span> wagtail.admin.edit_handlers <span class="k">import</span> StreamFieldPanel
<span class="k">from</span> wagtail.images.edit_handlers <span class="k">import</span> ImageChooserPanel
<span class="k">from</span> wagtail.contrib.modeladmin.options <span class="k">import</span> ModelAdmin
<span class="k">from</span> wagtail.contrib.settings.models <span class="k">import</span> BaseSetting
<span class="k">from</span> django.utils.translation <span class="k">import</span> ugettext_lazy <span class="k">as</span> _
<span class="k">from</span> django.conf.urls <span class="k">import</span> url

MIDDLEWARE = [ &hellip; <span class="s">'wagtail.core.middleware.SiteMiddleware'</span>, &hellip; ]</pre>
            """,
            say="And it is written exactly the way a twenty nineteen project was written. Wagtail core "
                "imports. Stream field panels and image chooser panels. Model admin. Base setting. "
                "Django's u get text lazy, the old url function, and the site middleware. Every one "
                "of these lines is about to break.",
        ),
        Scene(
            id="labels",
            body="""
            <div class="eyebrow">Keep an eye on these form labels</div>
            <pre class="code" style="font-size:40px"><span class="s">"Parent/Guardian's full name"</span>
<span class="s">"How did you hear about us?"</span>
<span class="s">"Languages spoken at home (e.g. Français, Español)"</span></pre>
            <div class="sub" style="margin-top:40px">Apostrophes, a slash, a question mark, accents.
            They come back later.</div>
            """,
            say="The enrolment form has labels with apostrophes, a slash, a question mark and accented "
                "characters. That is deliberate. Keep an eye on them. They come back later.",
        ),

        # ------------------------------------------------------------------ method
        Scene(
            id="baseline",
            body="""
            <div class="eyebrow">Before touching anything: a baseline</div>
            <ul class="bullets">
              <li>Every URL and its status <span class="dim">&mdash; 55</span></li>
              <li>The visible text of every page <span class="dim">&mdash; 51</span></li>
              <li>Form submissions, exported by Wagtail's own CSV export</li>
              <li>Full-page screenshots <span class="dim">&mdash; 29</span></li>
              <li>A database dump and a copy of media</li>
            </ul>
            """,
            say="Before touching anything, I recorded a baseline from the running site. Every U R L and "
                "its status. The visible text of every page, which is how you prove StreamField content "
                "survives. The form submissions, exported with Wagtail's own C S V export. Twenty nine "
                "screenshots. And a database dump. Every stage gets compared against this.",
        ),
        Scene(
            id="route",
            body=CSS + """
            <div class="eyebrow">The route</div>
            <div class="flow">
              <div class="v">2.7<small>2019 &middot; Django 2.2</small></div>
              <div class="arr">&rarr;</div>
              <div class="v">2.15 LTS<small>Django 3.2</small></div>
              <div class="arr">&rarr;</div>
              <div class="v">7.4 LTS<small>Django 5.2</small></div>
            </div>
            <div class="sub" style="margin-top:70px">Wagtail recommends one release at a time.
            I did two hops &mdash; the second one skips seventeen releases.</div>
            """,
            say="Wagtail recommends upgrading one release at a time. I did two hops. First to two fifteen, "
                "the long term support release that contains a big form builder change. Then straight to "
                "seven point four, skipping seventeen releases, because that is how I actually upgrade "
                "client sites. And I wanted to know what that costs.",
        ),

        # ------------------------------------------------------------------ hop 1
        Scene(
            id="hop1",
            classes="title-slide",
            body="""
            <div class="eyebrow">Hop one</div>
            <h1>2.7 &rarr; 2.15</h1>
            <div class="rule"></div>
            <div class="sub">Django 2.2 &rarr; 3.2 &nbsp;&middot;&nbsp; Python 3.8 &rarr; 3.10</div>
            """,
            say="Hop one. Two point seven to two fifteen.",
        ),
        # log 036
        terminal_scene(
            scene_id="b01_psycopg",
            eyebrow="B01 &middot; the first wall isn't Wagtail",
            title="",
            bar="pip install -r requirements.txt  &middot;  Python 3.10",
            steps=[
                Cmd(text="pip install -r requirements.txt", prompt=P215,
                    out="      building 'psycopg2._psycopg' extension\n"
                        "      error: Microsoft Visual C++ 14.0 or greater is required.\n"
                        "  ERROR: Failed building wheel for psycopg2-binary",
                    error=["error:", "ERROR"]),
            ],
            say="The first thing to break is not Wagtail. It is the database driver. Wagtail two fifteen "
                "is the first release that supports Python three ten, and the psycopg two driver from "
                "twenty nineteen has no build for it, so pip tries to compile it and asks for a C plus "
                "plus compiler. Bump it to two point nine and move on.",
        ),
        # logs 040, 045
        terminal_scene(
            scene_id="b03_middleware",
            eyebrow="B03 &middot; green checks, broken site",
            title="",
            bar="Wagtail 2.15 &middot; first request",
            steps=[
                Cmd(text="python manage.py check", prompt=P215,
                    out="System check identified no issues (0 silenced).", highlight=["no issues"]),
                Cmd(text="# ...then the first page request", prompt=P215,
                    out="ModuleNotFoundError: No module named 'wagtail.core.middleware'",
                    error=["ModuleNotFoundError"]),
            ],
            say="Then a classic. The system check says no issues. And the very first page request "
                "crashes. No module named wagtail core middleware. Middleware only loads when a request "
                "comes in, so the check never sees it.",
        ),
        Scene(
            id="b03_fix",
            body="""
            <div class="eyebrow">B03 &middot; SiteMiddleware &rarr; Site.find_for_request</div>
            <pre class="code" style="font-size:36px"><span class="c"># core/templatetags/navigation_tags.py</span>
<span class="bad">root = request.site.root_page</span>
<span class="k">root = Site.find_for_request(request).root_page</span></pre>
            <div class="sub" style="margin-top:36px">Deprecated in 2.9, moved in 2.11. Delete the
            middleware, ask the Site model instead.</div>
            """,
            say="Site middleware was deprecated in two point nine and moved in two eleven. The fix is "
                "one line. Instead of request dot site, ask the site model for the current site.",
        ),

        # ---- B04: the clean_name moment
        Scene(
            id="b04_how27",
            body="""
            <div class="eyebrow">B04 &middot; how Wagtail 2.7 stores form data</div>
            <pre class="code" style="font-size:34px"><span class="c"># the key is computed from the label, every time</span>
slugify(unidecode(<span class="s">"Parent/Guardian's full name"</span>))
  <span class="k">&rarr; "parentguardians-full-name"</span>

<span class="c"># Wagtail 2.10+: a stored field, generated differently</span>
clean_name  <span class="k">&rarr; "parentguardians_full_name"</span></pre>
            """,
            say="Now the big one. In Wagtail two point seven, each form submission is stored under a key "
                "that is computed from the field's label, every single time. Parent guardian's full "
                "name becomes parent guardians, dash, full, dash, name. Wagtail two point ten made that "
                "key a stored database field called clean name, and generates it differently, with "
                "underscores.",
        ),
        Scene(
            id="b04_addfield",
            body="""
            <div class="eyebrow">B04 &middot; the migration</div>
            <pre class="code" style="font-size:34px">migrations.AddField(
    model_name=<span class="s">'formfield'</span>, name=<span class="s">'clean_name'</span>,
    field=models.CharField(blank=<span class="k">True</span>, <span class="bad">default=''</span>, &hellip;))</pre>
            <div class="sub" style="margin-top:36px">No data migration. After <b>migrate</b>,
            all 14 form fields have an empty key.</div>
            """,
            say="Make migrations adds that field with an empty default, and no data migration. So after "
                "migrate, all fourteen form fields have an empty key. Here is what a production server "
                "then serves.",
        ),
        # log 048
        terminal_scene(
            scene_id="b04_broken",
            eyebrow="B04 &middot; a server that never ran system checks",
            title="",
            bar="Wagtail 2.15 &middot; enrolment form, admin, CSV export",
            steps=[
                Cmd(text="list(page.get_form().fields)", prompt=PY, out="['']", error=["''"]),
                Cmd(text="'example.com' in admin_submissions_listing", prompt=PY, out="False",
                    error=["False"]),
                Cmd(text="csv_export.splitlines()[:2]", prompt=PY,
                    out="Submission date,Subscribe to our newsletter,Subscribe to our newsletter,...\n"
                        "2026-03-27 21:06:16.451089+00:00,None,None,None,None,None,None,None,None,None,None",
                    error=["Subscribe", "None"]),
            ],
            say="The ten field enrolment form is now one field, named nothing. The admin submissions list "
                "shows none of the stored values. And the C S V export has ten columns, all called "
                "subscribe to our newsletter, and every value is none. The data is still in the "
                "database. Nothing can read it.",
        ),
        # log 049
        terminal_scene(
            scene_id="b04_check_crash",
            eyebrow="B04 &middot; the repair lives in a system check",
            title="",
            bar="Wagtail 2.15 &middot; manage.py check",
            steps=[
                Cmd(text="python manage.py check", prompt=P215,
                    out="Exception: You have form submission data that was created on an older\n"
                        "version of Wagtail and requires the unidecode library to retrieve it\n"
                        "correctly. Please install the unidecode package.",
                    error=["Exception", "version", "correctly"]),
            ],
            say="Wagtail does repair this. But inside a system check, not a migration. So I ran the check. "
                "And the repair itself crashes. It needs the unidecode library. Wagtail two point seven "
                "depended on it. Wagtail two fifteen does not. The upgrade removed the package the "
                "upgrade needs.",
        ),
        # logs 053, 054
        terminal_scene(
            scene_id="b04_fixed",
            eyebrow="B04 &middot; one package, one check",
            title="",
            bar="Wagtail 2.15 &middot; after pip install Unidecode",
            steps=[
                Cmd(text="python manage.py check", prompt=P215,
                    out="forms.ContactFormField: Added `clean_name` on 4 form field(s)\n"
                        "forms.FormField: Added `clean_name` on 10 form field(s)",
                    highlight=["Added"]),
                Cmd(text="python manage.py shell -c \"exec(open('tools/form_keys_report.py').read())\"",
                    prompt=P215,
                    out="Parent/Guardian's full name   clean_name='parentguardians-full-name'   matches data\n"
                        "Email address                 clean_name='email-address'               matches data",
                    highlight=["matches data"]),
            ],
            say="Install unidecode, run the check once more, and Wagtail backfills all fourteen keys with "
                "the old hyphenated names. Every key matches the stored data, and all thirty enquiries "
                "are back, in the form, the admin and the C S V.",
        ),
        Scene(
            id="b04_lessons",
            body="""
            <div class="eyebrow">B04 &middot; before you upgrade a form-builder site</div>
            <ul class="bullets">
              <li>Add <b>Unidecode</b> to requirements</li>
              <li>Run <b>manage.py check</b> on the server after deploying</li>
              <li class="off">Until something runs system checks, your live forms are broken</li>
              <li>New fields get <b>snake_case</b> keys &mdash; two naming styles, forever</li>
            </ul>
            """,
            say="So. Add unidecode to your requirements. Run manage dot py check on the server after you "
                "deploy, because until something runs the system checks, your live forms are broken. "
                "And know that any field you add later gets an underscore key, so one form ends up with "
                "two naming styles for good.",
        ),
        Scene(
            id="b05_csv",
            body="""
            <div class="eyebrow">B05 &middot; the export button that isn't</div>
            <pre class="code" style="font-size:36px"><span class="bad">/admin/forms/submissions/135/?action=CSV</span>   <span class="c">&rarr; 200 text/html</span>
<span class="k">/admin/forms/submissions/135/?export=csv</span>   <span class="c">&rarr; 200 text/csv</span></pre>
            <div class="sub" style="margin-top:36px">Not in the release notes. Any script or bookmark that
            downloads exports silently gets the HTML page instead.</div>
            """,
            say="One more quiet one. The admin's C S V export moved from action equals C S V to export "
                "equals C S V. The old address still returns two hundred, just with the H T M L page "
                "instead of the file. I could not find it in the release notes.",
        ),
        Scene(
            id="hop1_result",
            body=CSS + """
            <div class="eyebrow">Hop one &middot; result</div>
            <h2>Six breakages. Then byte for byte.</h2>
            <ul class="bullets">
              <li>Every URL status, page text and count identical to 2.7</li>
              <li>Both CSV exports identical, byte for byte</li>
              <li>12 front-end pages pixel-identical</li>
            </ul>
            """,
            say="Six breakages in hop one, including a database driver and a moved import in the seed "
                "command. After that, the crawl matched two point seven byte for byte, including both "
                "C S V exports, and twelve front end pages were pixel identical.",
        ),

        # ------------------------------------------------------------------ hop 2
        Scene(
            id="hop2",
            classes="title-slide",
            body="""
            <div class="eyebrow">Hop two &middot; skipping seventeen releases</div>
            <h1>2.15 &rarr; 7.4</h1>
            <div class="rule"></div>
            <div class="sub">Django 3.2 &rarr; 5.2 &nbsp;&middot;&nbsp; Python 3.10 &rarr; 3.12</div>
            """,
            say="Hop two. Two fifteen straight to seven point four. Installing it was the easy part. "
                "It worked first time.",
        ),
        Scene(
            id="import_wall",
            body=CSS + """
            <div class="eyebrow">The import wall &middot; manage.py check, eight times</div>
            <table class="small">
              <tr><th>Error</th><th>Fix</th></tr>
              <tr><td class="err">No module named 'wagtail.contrib.modeladmin'</td><td class="fix">PageListingViewSet</td></tr>
              <tr><td class="err">No module named 'wagtail.core'</td><td class="fix">wagtail updatemodulepaths</td></tr>
              <tr><td class="err">cannot import name 'ugettext_lazy'</td><td class="fix">gettext_lazy</td></tr>
              <tr><td class="err">cannot import name 'StreamFieldPanel'</td><td class="fix">FieldPanel</td></tr>
              <tr><td class="err">cannot import name 'BaseSetting'</td><td class="fix">BaseSiteSetting</td></tr>
              <tr><td class="err">cannot import name 'url'</td><td class="fix">re_path</td></tr>
              <tr><td class="err">cannot import name 'Query'</td><td class="fix">search_promotions</td></tr>
              <tr><td class="err">W003 WAGTAILADMIN_BASE_URL</td><td class="fix">rename BASE_URL</td></tr>
            </table>
            """,
            say="Then the check failed eight times in a row, one missing import at a time. Model admin. "
                "Wagtail core. u get text lazy. Stream field panel. Base setting. The url function. The "
                "search query model. And the base U R L setting. The surprise is that none of these "
                "printed a single deprecation warning on two fifteen.",
        ),
        # logs 084, 085
        terminal_scene(
            scene_id="updatemodulepaths",
            eyebrow="B08 &middot; the biggest diff, one command",
            title="",
            bar="Wagtail 7.4",
            steps=[
                Cmd(text="wagtail help updatemodulepaths", prompt=P74,
                    out="Update a Wagtail project tree to use Wagtail 2.x module paths"),
                Cmd(text="wagtail updatemodulepaths .", prompt=P74,
                    out="Checked 62 .py files, 19 files updated.", highlight=["19 files updated"]),
            ],
            say="The biggest change of the whole upgrade was a single command. Wagtail update module paths "
                "rewrote nineteen files, even inside old migrations. Its help text still says two point "
                "x. It does not replace the removed panel classes though. That part is by hand.",
        ),
        Scene(
            id="modeladmin_code",
            body="""
            <div class="eyebrow">B07 &middot; ModelAdmin &rarr; PageListingViewSet</div>
            <pre class="code" style="font-size:28px"><span class="k">class</span> EventPageListingViewSet(PageListingViewSet):
    index_view_class = EventPageListingIndexView   <span class="c"># default_ordering = 'start_date'</span>
    model = EventPage
    menu_label = <span class="s">'Events'</span>
    icon = <span class="s">'date'</span>
    add_to_admin_menu = <span class="k">True</span>
    list_display = [<span class="s">'title'</span>, <span class="s">'start_date'</span>, <span class="s">'category'</span>, <span class="s">'live'</span>]
    list_filter = [<span class="s">'category'</span>, <span class="s">'live'</span>]</pre>
            """,
            say="Model admin was removed in Wagtail six. Both of my model admins listed pages, and snippet "
                "view sets cannot register pages. The core replacement is the page listing view set. "
                "Same menu, same columns. One catch. It lists in tree order until you set a default "
                "ordering on the index view.",
        ),
        Scene(
            id="modeladmin_shot",
            body=CSS + f"""
            <div class="eyebrow">Same menu, new API</div>
            {img(BLOG_IMG / 'events-menu-modeladmin-vs-pagelistingviewset.png')}
            """,
            say="Here it is. Model admin on the left, the page listing view set on the right.",
        ),

        # ---- B15
        terminal_scene(
            scene_id="b15_green",
            eyebrow="B15 &middot; everything looks fine",
            title="",
            bar="Wagtail 7.4 &middot; restored 2.15 data",
            steps=[
                Cmd(text="python manage.py makemigrations", prompt=P74,
                    out="Migrations for 'forms':\n  ~ Alter field choices on contactformfield  ..."),
                Cmd(text="python manage.py migrate", prompt=P74, out="  ...64 migrations, all OK"),
                Cmd(text="client.get('/events/spring-open-morning/').status_code", prompt=PY, out="200",
                    highlight=["200"]),
            ],
            say="With the imports fixed, make migrations found only small form changes. Migrate ran sixty "
                "four migrations cleanly. Pages return two hundred. Everything looks fine.",
        ),
        # log 097
        terminal_scene(
            scene_id="b15_query",
            eyebrow="B15 &middot; then ask a JSON question",
            title="",
            bar="Wagtail 7.4 &middot; manage.py shell",
            steps=[
                Cmd(text="EventPage.objects.filter(body__contains=[{'type': 'call_to_action'}]).count()",
                    prompt=PY, out="ProgrammingError: operator does not exist: text @> jsonb",
                    error=["ProgrammingError"]),
            ],
            say="Then ask the database a JSON question about StreamField content. Operator does not "
                "exist. Text contains J S O N b. The body columns are still plain text.",
        ),
        Scene(
            id="b15_why",
            body="""
            <div class="eyebrow">B15 &middot; the migration that never came</div>
            <div class="cols">
              <div class="col"><h3>Wagtail 3.0 &ndash; 5.x</h3>
                <p>Add <b>use_json_field=True</b>. makemigrations writes an <b>AlterField</b> that
                converts the column from text to jsonb.</p></div>
              <div class="col hero"><h3>Wagtail 6.0+</h3>
                <p><b>use_json_field</b> is ignored and never appears in migrations. Django sees
                <b>no difference</b> &mdash; so the conversion is <b>never generated</b>.</p></div>
            </div>
            <div class="sub" style="margin-top:44px">Skip 3.0&ndash;5.x and a fresh database gets jsonb, while
            your upgraded one keeps text. No tool reports it.</div>
            """,
            say="Here is why. In Wagtail three to five, you added use jason field, and make migrations "
                "wrote a migration that converted the column to J S O N. From Wagtail six, that option is "
                "ignored and never appears in migrations. So if you skip three to five, the conversion "
                "is never generated. A fresh database gets J S O N. Your upgraded one keeps text. And "
                "no tool tells you.",
        ),
        Scene(
            id="b15_fix",
            body="""
            <div class="eyebrow">B15 &middot; write the migration yourself</div>
            <pre class="code" style="font-size:30px">migrations.RunSQL(
    sql=<span class="s">'ALTER TABLE events_eventpage ALTER COLUMN body TYPE jsonb USING body::jsonb'</span>,
    reverse_sql=<span class="s">'... TYPE text USING body::text'</span>,
)</pre>
            <div class="sub" style="margin-top:36px">One per app. A no-op on fresh databases.
            The query now returns <b>2</b> &mdash; the Open Day events.</div>
            """,
            say="The fix is a small hand written migration per app that converts the column in place. On "
                "a fresh database it does nothing. Afterwards, the same query returns two, the open day "
                "events that have a call to action.",
        ),

        # ---- B16
        terminal_scene(
            scene_id="b16_lost",
            eyebrow="B16 &middot; data lost by design",
            title="",
            bar="Wagtail 7.4 &middot; after migrate",
            steps=[
                Cmd(text="Query.objects.count(), QueryDailyHits.objects.count()", prompt=PY,
                    out="after migrate: queries = 0 , daily hits = 0", error=["= 0"]),
            ],
            say="The restored site had two logged search queries. After migrate, zero.",
        ),
        Scene(
            id="b16_source",
            body="""
            <div class="eyebrow">wagtail/contrib/search_promotions/migrations/0004_copy_queries.py</div>
            <pre class="code" style="font-size:31px"><span class="c"># Changed to a no-op in Wagtail 6.0.
# ... any project that needs this data migration would
# have already applied the real version of this migration
# while they were running Wagtail 5.</span>
operations = []</pre>
            """,
            say="The migration that should copy them has been a no-op since Wagtail six. The comment in "
                "its source says any project that needed it would already have run the real one, on "
                "Wagtail five. Skip Wagtail five, and this data is gone.",
        ),
        # log 103
        terminal_scene(
            scene_id="b16_recover",
            eyebrow="B16 &middot; recovered from the pre-upgrade dump",
            title="",
            bar="Wagtail 7.4",
            steps=[
                Cmd(text="python tools/recover_search_queries.py wagtail_school_215.dump", prompt=P74,
                    out="found 2 queries and 2 daily-hit rows in wagtail_school_215.dump\n"
                        "  query 'music': created\n"
                        "  query 'scholarship': created\n"
                        "now: 2 queries, 2 daily-hit rows",
                    highlight=["now:"]),
            ],
            say="I got it back only because I had taken a database dump before migrating.",
        ),
        Scene(
            id="b16_lesson",
            body="""
            <div class="quote">If you skip versions, <span class="hl">take a dump right before
            migrate</span> &mdash; and check every table you care about afterwards.</div>
            """,
            say="This is the strongest argument I found for upgrading one release at a time. And if you "
                "skip anyway, take a dump right before migrate, and check every table you care about "
                "afterwards.",
        ),

        # ---- B19
        Scene(
            id="b19_static",
            body="""
            <div class="eyebrow">B19 &middot; silently switched off</div>
            <pre class="code" style="font-size:30px"><span class="c"># settings/base.py, from 2019</span>
<span class="bad">STATICFILES_STORAGE = '...ManifestStaticFilesStorage'</span>   <span class="c"># Django 5.1: ignored</span>

<span class="c"># what Django 5.2 actually used</span>
STORAGES[<span class="s">'staticfiles'</span>] = {<span class="s">'BACKEND'</span>: <span class="s">'...StaticFilesStorage'</span>}</pre>
            <div class="sub" style="margin-top:36px">No error, no warning. No hashed filenames &mdash; stale
            CSS after every deploy.</div>
            """,
            say="Another silent one. The old static files storage setting was removed in Django five one, "
                "and Django ignores settings it does not know. No error, no warning. Production just "
                "stops getting hashed file names, and visitors keep seeing old C S S after every deploy.",
        ),

        # ---- B21, B22
        Scene(
            id="b21_radio",
            body=CSS + f"""
            <div class="eyebrow">B21 &middot; the only visible break &mdash; found by pixel diff</div>
            <div class="pair"><div class="lbl">Wagtail 2.7</div><div class="lbl bad">Wagtail 7.4, before the fix</div></div>
            {img(BLOG_IMG / 'radio-buttons-2.7-vs-7.4-before-fix.png')}
            """,
            say="On the front end, pixel diffing found exactly one visual break. The radio buttons and "
                "check boxes turned bold, with no gap.",
        ),
        Scene(
            id="b21_fix",
            body="""
            <div class="eyebrow">B21 &middot; Django 4.0 changed the widget markup</div>
            <pre class="code" style="font-size:32px"><span class="c">&lt;!-- Django 2.2 --&gt;</span>  &lt;ul&gt;&lt;li&gt;&lt;label&gt;&lt;input&gt; Term 1
<span class="c">&lt;!-- Django 4.0+ --&gt;</span> &lt;div&gt;&lt;div&gt;&lt;label&gt;&lt;input&gt; Term 1

<span class="bad">.school-form fieldset ul label { font-weight: 400; }</span>
<span class="k">.school-form fieldset &gt; div label { font-weight: 400; }</span></pre>
            <div class="sub" style="margin-top:32px">Retarget the CSS &rarr; <b>zero pixels</b> different.</div>
            """,
            say="Django four changed those widgets from a list to divs, so the twenty nineteen C S S "
                "stopped matching. Retarget two selectors, and the form is back to zero pixels different.",
        ),
        Scene(
            id="b22_wblock",
            body="""
            <div class="eyebrow">B22 &middot; StreamField classes in 7.4</div>
            <pre class="code" style="font-size:40px">&lt;div class=<span class="s">"<b>w-block-heading</b> block-heading"</span>&gt;</pre>
            <div class="sub" style="margin-top:40px">The old <b>block-*</b> class &ldquo;will be removed in a
            future release&rdquo;. Moved all 15 selectors to <b>.w-block-*</b> now &mdash; still
            pixel-identical.</div>
            """,
            say="And Wagtail seven four renames the StreamField block classes to w block. The old names "
                "still work, for now. I moved all fifteen selectors across, and the pages are still pixel "
                "identical.",
        ),
        Scene(
            id="the_rest",
            body="""
            <div class="eyebrow">And the rest</div>
            <ul class="bullets" style="margin-top:10px">
              <li>Submission data is a <b>dict</b> now &mdash; <span class="dim">json.loads() crashes</span></li>
              <li>Search got <b>better</b> &mdash; <span class="dim">7 results for "music" instead of 1</span></li>
              <li>A dependency I never declared &mdash; <span class="dim">unidecode, again</span></li>
              <li>Run <b>update_index</b> and <b>rebuild_references_index</b></li>
            </ul>
            """,
            say="The rest. Form submission data is now a dictionary, so any script that parses it crashes. "
                "Search got better, it now finds seven results for music instead of one. My own seed "
                "script imported unidecode without declaring it. And after upgrading, rebuild the "
                "search index and the references index.",
        ),

        # ------------------------------------------------------------------ result
        Scene(
            id="result",
            body=CSS + """
            <div class="eyebrow">2.7 &rarr; 7.4 &middot; the result</div>
            <table class="small">
              <tr><td class="k">URL statuses</td><td class="v">55 of 55 identical</td></tr>
              <tr><td class="k">Page text</td><td class="v">49 of 51 identical &mdash; 2 search pages find more</td></tr>
              <tr><td class="k">Form CSV exports</td><td class="v">byte-for-byte identical</td></tr>
              <tr><td class="k">Front-end screenshots</td><td class="v">11 of 13 pixel-identical</td></tr>
              <tr><td class="k">python -Wa manage.py check</td><td class="v">0 warnings</td></tr>
              <tr><td class="k">Fresh database + seed</td><td class="v">same counts as 2019</td></tr>
            </table>
            """,
            say="The result. Every U R L status identical. Forty nine of fifty one pages with identical "
                "text, and the other two are search pages finding more. Both C S V exports byte for byte "
                "identical. Eleven of thirteen front end pages pixel identical. And zero warnings.",
        ),
        Scene(
            id="home_compare",
            body=CSS + f"""
            <div class="eyebrow">Wagtail 2.7 (2019) &nbsp;&middot;&nbsp; Wagtail 7.4 &mdash; pixel-identical</div>
            {img(BLOG_IMG / 'home-2.7-vs-7.4.png')}
            """,
            say="Seven years of Wagtail, and the home page has not moved a single pixel.",
        ),
        Scene(
            id="editor_compare",
            body=CSS + f"""
            <div class="eyebrow">The editor, then and now</div>
            {img(BLOG_IMG / 'editor-2.7-vs-7.4.png')}
            """,
            say="The editor, on the other hand, is a completely different place to work.",
        ),

        # ------------------------------------------------------------------ checklist
        Scene(
            id="checklist_1",
            body="""
            <div class="eyebrow">If you're about to do this</div>
            <ul class="bullets">
              <li>Record a baseline first</li>
              <li>Form builder? Stop at 2.10&ndash;2.16, add Unidecode, run <b>check</b></li>
              <li>Pass through Wagtail 5 if you can</li>
              <li>Dump the database right before <b>migrate</b></li>
            </ul>
            """,
            say="If you are about to do this. Record a baseline first. If you use the form builder, stop "
                "somewhere between two ten and two sixteen, add unidecode, and run the check. Pass "
                "through Wagtail five if you can. And dump the database right before you migrate.",
        ),
        Scene(
            id="checklist_2",
            body="""
            <div class="eyebrow">If you're about to do this</div>
            <ul class="bullets">
              <li>Grep settings for names Django ignores</li>
              <li>Run <b>wagtail updatemodulepaths</b>, then fix what it can't</li>
              <li>Pixel-diff the front end</li>
              <li>Migrate and seed a fresh database too</li>
            </ul>
            """,
            say="Search your settings for names Django no longer reads. Run update module paths, then fix "
                "what it cannot. Pixel diff the front end. And migrate a fresh database too, because it "
                "finds the imports your live site never touches.",
        ),
        Scene(
            id="repo",
            body="""
            <div class="eyebrow">Everything is public</div>
            <h2>github.com/apequaltowork/wagtail-school</h2>
            <ul class="bullets">
              <li>One commit per step &mdash; follow the upgrade in order</li>
              <li>Tags: <b>v2.7-baseline</b> &middot; <b>v2.15</b> &middot; <b>v7.4</b></li>
              <li>Every log, every screenshot, the full breakage list, and the blog post</li>
            </ul>
            """,
            say="Everything is public. One commit per step, so you can follow the whole upgrade in order, "
                "with a tag for each stage. Every log, every screenshot, the full list of twenty two "
                "breakages, and the blog post that goes with this video.",
        ),
    ],
)
