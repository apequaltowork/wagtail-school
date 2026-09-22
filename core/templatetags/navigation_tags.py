from django import template

register = template.Library()


@register.inclusion_tag('core/tags/main_menu.html', takes_context=True)
def main_menu(context):
    request = context['request']
    calling_page = context.get('page') or context.get('self')
    root = request.site.root_page

    menuitems = root.get_children().live().in_menu()
    for menuitem in menuitems:
        menuitem.menu_children = menuitem.get_children().live().in_menu()
        menuitem.active = bool(
            calling_page and calling_page.url_path.startswith(menuitem.url_path)
        )

    return {
        'root': root,
        'menuitems': menuitems,
        'calling_page': calling_page,
        'request': request,
    }


@register.inclusion_tag('core/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    page = context.get('page') or context.get('self')
    if page is None or page.depth <= 2:
        ancestors = []
    else:
        ancestors = page.get_ancestors(inclusive=True).filter(depth__gt=1)
    return {
        'ancestors': ancestors,
        'request': context['request'],
    }
