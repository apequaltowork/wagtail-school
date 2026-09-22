from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import EventPage


class EventPageAdmin(ModelAdmin):
    model = EventPage
    menu_label = 'Events'
    menu_icon = 'date'
    menu_order = 200
    list_display = ('title', 'start_date', 'category', 'live')
    list_filter = ('category', 'live')
    search_fields = ('title', 'summary')
    ordering = ('start_date',)


modeladmin_register(EventPageAdmin)
