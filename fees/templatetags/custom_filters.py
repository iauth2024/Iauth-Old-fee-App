from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key, 0)

@register.filter(name='indian_number_format')
def indian_number_format(value):
    try:
        value = int(float(value))  # Convert to float first to handle decimal strings, then to int
    except ValueError:
        return value

    orig = str(value)
    if len(orig) <= 3:
        return orig

    last_three = orig[-3:]
    other_digits = orig[:-3]
    groups = []
    while other_digits:
        groups.append(other_digits[-2:])
        other_digits = other_digits[:-2]

    formatted = ','.join(reversed(groups)) + ',' + last_three
    return formatted

@register.filter(name='to_float')
def to_float(value):
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0
