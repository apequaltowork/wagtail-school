import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from modelcluster.fields import ParentalKey
from wagtail.admin.panels import (
    FieldPanel, InlinePanel, MultiFieldPanel, PageChooserPanel
)
from wagtail.fields import StreamField
from wagtail.models import Orderable, Page

from core.blocks import BaseStreamBlock


class HomePage(Page):
    hero_title = models.CharField(_('hero title'), max_length=255, blank=True)
    hero_intro = models.TextField(_('hero intro'), blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    cta_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name=_('call to action page'),
    )
    cta_label = models.CharField(_('call to action label'), max_length=100, blank=True)
    body = StreamField(BaseStreamBlock(), blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('hero_title'),
            FieldPanel('hero_intro'),
            FieldPanel('hero_image'),
        ], heading=_('Hero')),
        MultiFieldPanel([
            PageChooserPanel('cta_page'),
            FieldPanel('cta_label'),
        ], heading=_('Call to action')),
        InlinePanel('quick_links', label=_('Quick links')),
        FieldPanel('body'),
    ]

    max_count = 1

    def get_upcoming_events(self):
        from events.models import EventPage
        return EventPage.objects.live().filter(
            start_date__gte=datetime.date.today()
        ).select_related('category', 'image').order_by('start_date', 'start_time')[:3]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context['upcoming_events'] = self.get_upcoming_events()
        return context


class HomePageQuickLink(Orderable):
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='quick_links')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    link_url = models.URLField(blank=True, help_text=_('Used if no page is chosen'))

    panels = [
        FieldPanel('title'),
        FieldPanel('description'),
        PageChooserPanel('link_page'),
        FieldPanel('link_url'),
    ]

    @property
    def link(self):
        if self.link_page:
            return self.link_page.url
        return self.link_url
