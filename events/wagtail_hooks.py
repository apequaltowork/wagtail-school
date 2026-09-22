from wagtail import hooks
from wagtail.admin.views.pages.listing import IndexView
from wagtail.admin.viewsets.pages import PageListingViewSet

from .models import EventPage


class EventPageListingIndexView(IndexView):
    # ModelAdmin had ordering = ('start_date', ...)
    default_ordering = 'start_date'


class EventPageListingViewSet(PageListingViewSet):
    index_view_class = EventPageListingIndexView
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
