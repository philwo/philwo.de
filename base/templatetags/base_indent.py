from django.template.defaultfilters import stringfilter
from django import template

register = template.Library()


@register.filter(name='indent')
@stringfilter
def indent(value, arg=1):
    """
    Template filter to add the given number of tabs to the beginning of
    each line. Useful for keeping markup pretty, plays well with Markdown.

    Usage:
    {{ content|indent:"2" }}
    {{ content|markdown|indent:"2" }}
    """
    import re
    regex = re.compile("^", re.M)
    lines = value.split('\n')
    return lines[0] + '\n' + re.sub(regex, " " * int(arg), '\n'.join(lines[1:]))
