# myapp/templatetags/extra_filters.py
from django import template

register = template.Library()

@register.filter
def indian_number_format(value):
    try:
        value = float(value)
        return "{:,.0f}".format(value).replace(",", ",")
    except (ValueError, TypeError):
        return value
