from wagtail import hooks
from wagtail.admin.viewsets.pages import PageListingViewSet

from .models import StaffPage


class StaffPageListingViewSet(PageListingViewSet):
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
