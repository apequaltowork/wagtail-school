from wagtail import hooks
from wagtail.admin.views.pages.listing import IndexView
from wagtail.admin.viewsets.pages import PageListingViewSet

from .models import StaffPage


class StaffPageListingIndexView(IndexView):
    # ModelAdmin had ordering = ('department', ...)
    default_ordering = 'department'


class StaffPageListingViewSet(PageListingViewSet):
    index_view_class = StaffPageListingIndexView
    model = StaffPage
    name = 'staff'
    menu_label = 'Staff'
    icon = 'group'
    menu_order = 210
    add_to_admin_menu = True
    list_display = ['title', 'role', 'department']
    list_filter = ['department']


@hooks.register('register_admin_viewset')
def register_staff_listing():
    return StaffPageListingViewSet()
