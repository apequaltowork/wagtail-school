from django.db import models
from django.utils.translation import ugettext_lazy as _

from wagtail.admin.panels import FieldPanel, StreamFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.search import index

from core.blocks import BaseStreamBlock


class StandardPage(Page):
    intro = models.TextField(_('intro'), blank=True)
    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    body = StreamField(BaseStreamBlock(), blank=True)

    search_fields = Page.search_fields + [
        index.SearchField('intro'),
        index.SearchField('body'),
    ]

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname='full'),
        ImageChooserPanel('hero_image'),
        StreamFieldPanel('body'),
    ]
