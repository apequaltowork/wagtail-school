from itertools import groupby

from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.panels import FieldPanel, FieldRowPanel, MultiFieldPanel
from wagtail.fields import RichTextField
from wagtail.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet


@register_snippet
class Department(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    order = models.PositiveIntegerField(_('order'), default=0)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('order'),
    ]

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _('department')

    def __str__(self):
        return self.name


class StaffIndexPage(Page):
    intro = RichTextField(_('intro'), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    subpage_types = ['staff.StaffPage']

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        staff = StaffPage.objects.live().child_of(self).select_related(
            'department', 'photo'
        ).order_by('department__order', 'last_name', 'first_name')

        department = None
        department_slug = request.GET.get('department')
        if department_slug:
            department = Department.objects.filter(slug=department_slug).first()
            if department:
                staff = staff.filter(department=department)

        context['departments'] = Department.objects.all()
        context['current_department'] = department
        context['staff_groups'] = [
            (dept, list(members))
            for dept, members in groupby(staff, key=lambda member: member.department)
        ]
        return context


class StaffPage(Page):
    first_name = models.CharField(_('first name'), max_length=100)
    last_name = models.CharField(_('last name'), max_length=100)
    role = models.CharField(_('role'), max_length=255)
    department = models.ForeignKey(
        'staff.Department',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='staff'
    )
    photo = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    email = models.EmailField(_('email'), blank=True)
    phone_extension = models.CharField(_('phone extension'), max_length=10, blank=True)
    qualifications = models.CharField(_('qualifications'), max_length=255, blank=True)
    bio = RichTextField(_('bio'), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('first_name'),
        index.SearchField('last_name'),
        index.SearchField('role'),
        index.SearchField('bio'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('first_name', classname='col6'),
                FieldPanel('last_name', classname='col6'),
            ]),
            FieldPanel('role'),
            SnippetChooserPanel('department'),
        ], heading=_('Name and role')),
        ImageChooserPanel('photo'),
        MultiFieldPanel([
            FieldPanel('email'),
            FieldPanel('phone_extension'),
            FieldPanel('qualifications'),
        ], heading=_('Contact and qualifications')),
        FieldPanel('bio', classname='full'),
    ]

    parent_page_types = ['staff.StaffIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = _('staff member')

    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)
