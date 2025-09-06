from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def nav_class(context, page):
    request = context.get('request')
    active = None
    if request:
        active = (request.resolver_match.url_name == page) or (page == 'blog' and request.resolver_match.app_name == 'blog')
    else:
        active = False
    return ' active-nav-link' if active else ' inactive-nav-link'