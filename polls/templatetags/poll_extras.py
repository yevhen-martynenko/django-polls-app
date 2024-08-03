from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag(takes_context=True)
def breadcrumbs(context, path):
    parts = path.strip('/').split('/')
    output = ''
    full_link = ''

    for i, part in enumerate(parts):
        link = f'/{parts[i]}'
        full_link += link
        # TODO check if link is valid
        output += f"<a href=\'{full_link}\'>{part}</a>/"

    return mark_safe(output)
