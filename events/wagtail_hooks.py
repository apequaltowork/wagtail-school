from wagtail import hooks
from wagtail.admin.viewsets.pages import PageListingViewSet

from .models import EventPage


class EventPageListingViewSet(PageListingViewSet):
    model = EventPage
    name = 'events'
    menu_label = 'Events'
    icon = 'date'
    menu_order = 200
    add_to_admin_menu = True
    list_display = ['title', 'start_date', 'category', 'live']
    list_filter = ['category', 'live']


@hooks.register('register_admin_viewset')
def register_event_listing():
    return EventPageListingViewSet()
