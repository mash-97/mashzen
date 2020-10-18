from django import template
register = template.Library()

@register.filter
def enum(lst):
    return [(x+1, y) for x,y in enumerate(lst)]
