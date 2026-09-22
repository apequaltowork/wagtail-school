import datetime

from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import models
from django.template.response import TemplateResponse
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import (
    FieldPanel, FieldRowPanel, MultiFieldPanel, StreamFieldPanel
)
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet

from core.blocks import BaseStreamBlock


@register_snippet
class EventCategory(models.Model):
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    colour = models.CharField(
        _('colour'), max_length=7, default='#14284b',
        help_text=_('Hex colour used for the category badge, e.g. #14284b'),
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('colour'),
    ]

    class Meta:
        ordering = ['name']
        verbose_name = _('event category')
        verbose_name_plural = _('event categories')

    def __str__(self):
        return self.name


class EventIndexPage(RoutablePageMixin, Page):
    intro = RichTextField(_('intro'), blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
    ]

    subpage_types = ['events.EventPage']

    events_per_page = 6

    def get_events(self):
        return EventPage.objects.live().descendant_of(self).select_related('category', 'image')

    def paginate(self, request, queryset):
        paginator = Paginator(queryset, self.events_per_page)
        try:
            return paginator.page(request.GET.get('page', 1))
        except PageNotAnInteger:
            return paginator.page(1)
        except EmptyPage:
            return paginator.page(paginator.num_pages)

    def render_listing(self, request, events, listing):
        category = None
        category_slug = request.GET.get('category')
        if category_slug:
            category = EventCategory.objects.filter(slug=category_slug).first()
            if category:
                events = events.filter(category=category)

        context = self.get_context(request)
        context.update({
            'events': self.paginate(request, events),
            'categories': EventCategory.objects.all(),
            'current_category': category,
            'listing': listing,
        })
        return TemplateResponse(request, self.get_template(request), context)

    @route(r'^$')
    def upcoming_events(self, request):
        events = self.get_events().filter(
            start_date__gte=datetime.date.today()
        ).order_by('start_date', 'start_time')
        return self.render_listing(request, events, 'upcoming')

    @route(r'^past/$')
    def past_events(self, request):
        events = self.get_events().filter(
            start_date__lt=datetime.date.today()
        ).order_by('-start_date', '-start_time')
        return self.render_listing(request, events, 'past')


class EventPage(Page):
    start_date = models.DateField(_('start date'))
    end_date = models.DateField(_('end date'), null=True, blank=True)
    start_time = models.TimeField(_('start time'), null=True, blank=True)
    end_time = models.TimeField(_('end time'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=255, blank=True)
    category = models.ForeignKey(
        'events.EventCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='events'
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    summary = models.TextField(_('summary'), blank=True)
    body = StreamField(BaseStreamBlock(), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('summary'),
        index.SearchField('body'),
        index.SearchField('location'),
        index.FilterField('start_date'),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('start_date', classname='col6'),
                FieldPanel('end_date', classname='col6'),
            ]),
            FieldRowPanel([
                FieldPanel('start_time', classname='col6'),
                FieldPanel('end_time', classname='col6'),
            ]),
            FieldPanel('location'),
        ], heading=_('When and where')),
        SnippetChooserPanel('category'),
        ImageChooserPanel('image'),
        FieldPanel('summary'),
        StreamFieldPanel('body'),
    ]

    parent_page_types = ['events.EventIndexPage']
    subpage_types = []

    class Meta:
        verbose_name = _('event')

    @property
    def is_past(self):
        return (self.end_date or self.start_date) < datetime.date.today()
