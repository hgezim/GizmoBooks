import urllib
from django import template
register = template.Library()

@register.simple_tag
def active(request, pattern):
    pattern = urllib.unquote(pattern)
    if request.path.startswith(pattern):
        return 'active'
    return ''