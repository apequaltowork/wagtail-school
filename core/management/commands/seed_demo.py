import datetime
import json
import os
import random
import re
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files import File
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.http import QueryDict
from django.utils import timezone
from unidecode import unidecode

from wagtail.contrib.forms.models import FormSubmission
from wagtail.core.models import Page, Site
from wagtail.documents.models import get_document_model
from wagtail.images import get_image_model

from core import seed_data, seed_pages
from core.models import SchoolSettings
from events.models import EventCategory, EventIndexPage, EventPage
from forms.models import ContactFormField, ContactPage, FormField, FormPage
from home.models import HomePage, HomePageQuickLink
from pages.models import StandardPage
from staff.models import Department, StaffIndexPage, StaffPage

ASSETS = os.path.join(settings.BASE_DIR, 'seed', 'assets')
LINK_RE = re.compile(r'\[\[([\w-]+)\|([^\]]+)\]\]')
RANDOM_SEED = 2019


class Command(BaseCommand):
    help = 'Build the Kestrel Ridge College demo content (pages, media, snippets, settings, form submissions).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset', action='store_true',
            help='Delete the existing demo content and build it again.',
        )

    def handle(self, *args, **options):
        password = os.environ.get('DEMO_ADMIN_PASSWORD')
        if not password:
            raise CommandError('Set the DEMO_ADMIN_PASSWORD environment variable first.')

        self.home = HomePage.objects.first()
        if self.home is None:
            raise CommandError('No HomePage found. Run migrate first.')

        if options['reset']:
            with transaction.atomic():
                self.reset()
        elif self.home.get_children().exists():
            self.admin = self.ensure_admin(password)
            self.stdout.write('Demo content already exists. Use --reset to rebuild it.')
            return

        with transaction.atomic():
            self.admin = self.ensure_admin(password)
            self.rng = random.Random(RANDOM_SEED)
            self.pages = {}
            self.images = {}
            self.documents = {}

            self.create_media()
            self.create_snippets()
            self.create_settings()
            self.create_pages()
            self.fill_bodies()
            self.create_submissions()

        self.report()

    # ------------------------------------------------------------------
    # Reset
    # ------------------------------------------------------------------

    def reset(self):
        self.stdout.write('Removing existing demo content...')
        for child in self.home.get_children():
            child.delete()
        FormSubmission.objects.all().delete()
        HomePageQuickLink.objects.all().delete()
        get_image_model().objects.all().delete()
        get_document_model().objects.all().delete()
        EventCategory.objects.all().delete()
        Department.objects.all().delete()
        SchoolSettings.objects.all().delete()
        self.home = HomePage.objects.get(pk=self.home.pk)

    def ensure_admin(self, password):
        User = get_user_model()
        user = User.objects.filter(username='admin').first()
        if user is None:
            user = User.objects.create_superuser('admin', 'admin@kestrelridge.example', password)
            self.stdout.write('Created superuser "admin".')
        else:
            user.set_password(password)
            user.is_superuser = user.is_staff = True
            user.save()
        user.first_name, user.last_name = 'Site', 'Administrator'
        user.save()
        return user

    # ------------------------------------------------------------------
    # Media, snippets and settings
    # ------------------------------------------------------------------

    def add_image(self, filename, title):
        Image = get_image_model()
        with open(os.path.join(ASSETS, 'images', filename), 'rb') as f:
            image = Image(title=title)
            image.file.save(filename, File(f), save=False)
            image.save()
        return image

    def create_media(self):
        for key, filename, title in seed_data.BANNERS:
            self.images[key] = self.add_image(filename, title)
        for name, slug, _colour, filename in seed_data.CATEGORIES:
            self.images['category-' + slug] = self.add_image(filename, '{} events'.format(name))
        for member in seed_data.STAFF:
            filename = seed_data.staff_photo_filename(member)
            self.images[filename] = self.add_image(
                filename, '{} {}'.format(member['first_name'], member['last_name'])
            )

        Document = get_document_model()
        for key, filename, title in seed_data.DOCUMENTS:
            with open(os.path.join(ASSETS, 'documents', filename), 'rb') as f:
                document = Document(title=title)
                document.file.save(filename, File(f), save=False)
                document.save()
            self.documents[key] = document

    def create_snippets(self):
        self.categories = {}
        for name, slug, colour, _filename in seed_data.CATEGORIES:
            self.categories[slug] = EventCategory.objects.create(name=name, slug=slug, colour=colour)
        self.departments = {}
        for name, slug, order in seed_data.DEPARTMENTS:
            self.departments[slug] = Department.objects.create(name=name, slug=slug, order=order)

    def create_settings(self):
        site = Site.objects.get(is_default_site=True)
        site.site_name = seed_data.SCHOOL['school_name']
        site.save()
        school = SchoolSettings.for_site(site)
        for field, value in seed_data.SCHOOL.items():
            setattr(school, field, value)
        school.save()

    # ------------------------------------------------------------------
    # Pages
    # ------------------------------------------------------------------

    def publish(self, page):
        page.save_revision(user=self.admin).publish()

    def add_page(self, parent, page):
        parent.add_child(instance=page)
        self.pages[page.slug] = page
        return page

    def create_pages(self):
        home = self.home

        for parent_slug, slug, title, in_menu, banner, intro, _body in seed_pages.STANDARD_PAGES:
            parent = self.pages[parent_slug] if parent_slug else home
            self.add_page(parent, StandardPage(
                title=title, slug=slug, show_in_menus=in_menu, intro=intro,
                search_description=intro, hero_image=self.images[banner],
            ))
            if slug == 'admissions':
                self.create_enquiry_page()

        index = seed_pages.EVENT_INDEX
        events_index = self.add_page(home, EventIndexPage(
            title=index['title'], slug=index['slug'], show_in_menus=True, intro=index['intro'],
        ))
        self.create_events(events_index)

        index = seed_pages.STAFF_INDEX
        staff_index = self.add_page(home, StaffIndexPage(
            title=index['title'], slug=index['slug'], show_in_menus=True, intro=index['intro'],
        ))
        self.create_staff(staff_index)

        self.create_contact_page()

    def create_enquiry_page(self):
        spec = seed_pages.ENQUIRY_PAGE
        page = FormPage(
            title=spec['title'], slug=spec['slug'], show_in_menus=True, intro=spec['intro'],
            thank_you_text='', to_address=spec['to_address'], from_address=spec['from_address'],
            subject=spec['subject'],
        )
        page.form_fields = [
            FormField(sort_order=i, label=label, field_type=field_type, required=required, choices=choices)
            for i, (label, field_type, required, choices) in enumerate(seed_data.ENQUIRY_FIELDS)
        ]
        self.add_page(self.pages[spec['parent']], page)

    def create_contact_page(self):
        spec = seed_pages.CONTACT_PAGE
        page = ContactPage(
            title=spec['title'], slug=spec['slug'], show_in_menus=True, intro=spec['intro'],
            thank_you_text='', to_address=spec['to_address'], from_address=spec['from_address'],
            subject=spec['subject'],
        )
        page.form_fields = [
            ContactFormField(sort_order=i, label=label, field_type=field_type, required=required, choices=choices)
            for i, (label, field_type, required, choices) in enumerate(seed_data.CONTACT_FIELDS)
        ]
        self.add_page(self.home, page)

    def create_events(self, index):
        today = datetime.date.today()
        for spec in seed_data.EVENTS:
            start = today + datetime.timedelta(days=spec['offset'])
            self.add_page(index, EventPage(
                title=spec['title'], slug=spec['slug'],
                start_date=start,
                end_date=start + datetime.timedelta(days=spec['length']) if spec['length'] else None,
                start_time=datetime.datetime.strptime(spec['start'], '%H:%M').time(),
                end_time=datetime.datetime.strptime(spec['end'], '%H:%M').time(),
                location=spec['location'],
                category=self.categories[spec['category']],
                image=self.images['category-' + spec['category']],
                summary=spec['summary'],
                search_description=spec['summary'],
            ))

    def create_staff(self, index):
        for member in seed_data.STAFF:
            first, last = member['first_name'], member['last_name']
            slug = unidecode('{}-{}'.format(first, last)).lower().replace("'", '')
            self.add_page(index, StaffPage(
                title='{} {}'.format(first, last), slug=slug,
                first_name=first, last_name=last, role=member['role'],
                department=self.departments[member['department']],
                photo=self.images[seed_data.staff_photo_filename(member)],
                email='{}.{}@kestrelridge.example'.format(
                    unidecode(first).lower(), unidecode(last).lower().replace("'", '')
                ),
                phone_extension=member['ext'],
                qualifications=member['qualifications'],
                bio=''.join('<p>{}</p>'.format(p) for p in member['bio']),
                search_description='{}, Kestrel Ridge College'.format(member['role']),
            ))

    # ------------------------------------------------------------------
    # Bodies (second pass, so internal links and CTAs can point at any page)
    # ------------------------------------------------------------------

    def rich(self, html):
        def link(match):
            return '<a linktype="page" id="{}">{}</a>'.format(self.pages[match.group(1)].pk, match.group(2))
        return LINK_RE.sub(link, html)

    def stream(self, blocks):
        data = []
        for block in blocks:
            kind = block[0]
            if kind == 'heading':
                value = {'text': block[1], 'size': block[2] if len(block) > 2 else 'h2'}
            elif kind == 'paragraph':
                value = self.rich(block[1])
            elif kind == 'image':
                value = {'image': self.images[block[1]].pk, 'caption': block[2], 'alt_text': block[3]}
            elif kind == 'quote':
                value = {'text': block[1], 'attribution': block[2]}
            elif kind == 'cta':
                kind = 'call_to_action'
                value = {'heading': block[1], 'text': block[2], 'page': self.pages[block[3]].pk,
                         'button_label': block[4]}
            elif kind == 'document':
                value = {'document': self.documents[block[1]].pk, 'label': block[2]}
            elif kind == 'table':
                value = {'data': block[1], 'first_row_is_table_header': True,
                         'first_col_is_header': False, 'table_caption': ''}
            else:
                raise CommandError('Unknown block type {}'.format(kind))
            data.append({'type': kind, 'value': value, 'id': str(uuid.UUID(int=self.rng.getrandbits(128)))})
        return json.dumps(data)

    def fill_bodies(self):
        home = self.home
        spec = seed_pages.HOME
        home.hero_title = spec['hero_title']
        home.hero_intro = spec['hero_intro']
        home.hero_image = self.images[spec['hero_image']]
        home.cta_page = self.pages[spec['cta_page']]
        home.cta_label = spec['cta_label']
        home.seo_title = 'Kestrel Ridge College | Independent K-12 School'
        home.search_description = spec['hero_intro']
        home.quick_links = [
            HomePageQuickLink(sort_order=i, title=title, description=description, link_page=self.pages[slug])
            for i, (title, description, slug) in enumerate(spec['quick_links'])
        ]
        home.body = self.stream(spec['body'])
        self.publish(home)

        for _parent, slug, _title, _menu, _banner, _intro, body in seed_pages.STANDARD_PAGES:
            page = self.pages[slug]
            page.body = self.stream(body)
            self.publish(page)

        for spec in seed_data.EVENTS:
            page = self.pages[spec['slug']]
            blocks = [('paragraph', ''.join('<p>{}</p>'.format(p) for p in spec['body']))]
            if spec['category'] == 'open-day':
                blocks.append(('cta', 'Can\'t make it?', 'Make an enquiry and we will arrange a personal tour.',
                               'enrolment-enquiry', 'Make an enquiry'))
            page.body = self.stream(blocks)
            self.publish(page)

        for key in ('events', 'our-staff'):
            self.publish(self.pages[key])
        for page in StaffPage.objects.all():
            self.publish(page)

        for spec, model in ((seed_pages.ENQUIRY_PAGE, FormPage), (seed_pages.CONTACT_PAGE, ContactPage)):
            page = model.objects.get(pk=self.pages[spec['slug']].pk)
            page.thank_you_text = self.rich(spec['thank_you_text'])
            self.publish(page)

    # ------------------------------------------------------------------
    # Form submissions, through Wagtail's own form code path
    # ------------------------------------------------------------------

    def submit(self, page, values_by_label):
        blank_form = page.get_form(page=page, user=AnonymousUser())
        name_for_label = {field.label: name for name, field in blank_form.fields.items()}

        data = QueryDict(mutable=True)
        for label, value in values_by_label.items():
            name = name_for_label[label]
            if isinstance(value, list):
                data.setlist(name, value)
            elif value is True:
                data[name] = 'on'
            elif value:
                data[name] = value

        form = page.get_form(data, page=page, user=AnonymousUser())
        if not form.is_valid():
            raise CommandError('Seed submission for {} is invalid: {}'.format(page.slug, form.errors.as_json()))
        return page.process_form_submission(form)

    def person(self):
        first = self.rng.choice(seed_data.PARENT_FIRST_NAMES)
        last = self.rng.choice(seed_data.PARENT_LAST_NAMES)
        email = '{}.{}@example.com'.format(unidecode(first).lower(), unidecode(last).lower().replace(' ', ''))
        return '{} {}'.format(first, last), email

    def create_submissions(self):
        rng = self.rng
        enquiry = FormPage.objects.get(slug=seed_pages.ENQUIRY_PAGE['slug'])
        contact = ContactPage.objects.get(slug=seed_pages.CONTACT_PAGE['slug'])
        labels = [field[0] for field in seed_data.ENQUIRY_FIELDS]

        jobs = []
        for i in range(30):
            name, email = self.person()
            heard = rng.sample(seed_data.HEARD_ABOUT, rng.choice([1, 1, 2]))
            jobs.append((enquiry, {
                labels[0]: name,
                labels[1]: email,
                labels[2]: '(02) 5550 {:04d}'.format(rng.randint(2000, 9999)) if rng.random() < .8 else '',
                labels[3]: rng.choice(seed_data.STUDENT_FIRST_NAMES),
                labels[4]: rng.choice(seed_data.YEAR_LEVELS),
                labels[5]: rng.choice(seed_data.TERMS),
                labels[6]: rng.choice(seed_data.LANGUAGES),
                labels[7]: [choice for choice in seed_data.HEARD_ABOUT if choice in heard],
                labels[8]: rng.choice(seed_data.ENQUIRY_COMMENTS),
                labels[9]: rng.random() < .6,
            }))

        for subject, message in seed_data.CONTACT_MESSAGES:
            name, email = self.person()
            jobs.append((contact, {
                'Your name': name, 'Email': email, 'Subject': subject, 'Message': message,
            }))

        # Interleave the two forms, submit in that order, then spread submit_time
        # over the last six months so newer submissions have later times.
        rng.shuffle(jobs)
        submissions = [self.submit(page, values) for page, values in jobs]
        now = timezone.now()
        times = sorted(
            now - datetime.timedelta(days=rng.uniform(1, 182), minutes=rng.randint(0, 600))
            for _ in submissions
        )
        for submission, submit_time in zip(submissions, times):
            FormSubmission.objects.filter(pk=submission.pk).update(submit_time=submit_time)

    # ------------------------------------------------------------------

    def report(self):
        Image, Document = get_image_model(), get_document_model()
        self.stdout.write(self.style.SUCCESS('Demo content ready:'))
        rows = [
            ('Pages (live, excluding root)', Page.objects.live().filter(depth__gt=1).count()),
            ('  StandardPage', StandardPage.objects.count()),
            ('  EventPage', EventPage.objects.count()),
            ('  StaffPage', StaffPage.objects.count()),
            ('Images', Image.objects.count()),
            ('Documents', Document.objects.count()),
            ('Event categories', EventCategory.objects.count()),
            ('Departments', Department.objects.count()),
            ('Enquiry submissions', FormSubmission.objects.filter(page__slug='enrolment-enquiry').count()),
            ('Contact submissions', FormSubmission.objects.filter(page__slug='contact-us').count()),
        ]
        for label, count in rows:
            self.stdout.write('  {:<32} {}'.format(label, count))
