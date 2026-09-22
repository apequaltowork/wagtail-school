from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import StaffPage


class StaffPageAdmin(ModelAdmin):
    model = StaffPage
    menu_label = 'Staff'
    menu_icon = 'group'
    menu_order = 210
    list_display = ('full_name', 'role', 'department')
    list_filter = ('department',)
    search_fields = ('first_name', 'last_name', 'role')
    ordering = ('department__order', 'last_name')

    def full_name(self, obj):
        return obj.full_name
    full_name.short_description = 'Name'
    full_name.admin_order_field = 'last_name'


modeladmin_register(StaffPageAdmin)
