from django import template

register = template.Library()


@register.filter(name="get")
def get(d, k):
    return d.get(k, {})


@register.filter(name="leading_zeros")
def leading_zeros(value, desired_digits):
    num_zeros = int(desired_digits) - len(str(value))
    padded_value = []
    while num_zeros >= 1:
        padded_value.append("0")
        num_zeros -= num_zeros
    padded_value.append(str(value))
    return "".join(padded_value)


@register.filter
def divide(value, arg):
    try:
        result = float(value) / float(arg)
        return float("%.3f" % result)
    except (ValueError, ZeroDivisionError):
        return None
