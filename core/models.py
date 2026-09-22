from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting


@register_setting(icon='site')
class SchoolSettings(BaseSiteSetting):
    school_name = models.CharField(_('school name'), max_length=255, default='Kestrel Ridge College')
    address = models.TextField(_('address'), blank=True)
    phone = models.CharField(_('phone'), max_length=50, blank=True)
    email = models.EmailField(_('email'), blank=True)
    office_hours = models.TextField(_('office hours'), blank=True)
    map_embed_url = models.URLField(
        _('map embed URL'), max_length=500, blank=True,
        help_text=_('The src of an embeddable map iframe'),
    )

    facebook_url = models.URLField(_('Facebook URL'), blank=True)
    instagram_url = models.URLField(_('Instagram URL'), blank=True)
    youtube_url = models.URLField(_('YouTube URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)

    footer_text = models.TextField(_('footer text'), blank=True)

    panels = [
        FieldPanel('school_name'),
        MultiFieldPanel([
            FieldPanel('address'),
            FieldPanel('phone'),
            FieldPanel('email'),
            FieldPanel('office_hours'),
            FieldPanel('map_embed_url'),
        ], heading=_('Contact details')),
        MultiFieldPanel([
            FieldPanel('facebook_url'),
            FieldPanel('instagram_url'),
            FieldPanel('youtube_url'),
            FieldPanel('linkedin_url'),
        ], heading=_('Social media')),
        FieldPanel('footer_text'),
    ]

    class Meta:
        verbose_name = _('school settings')
