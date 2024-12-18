from django import template

register = template.Library()


@register.filter
def getattr_with_index(obj, attr):
    """Returns the value of obj.attr where attr is a dynamic attribute like 'option1', 'option2', etc."""
    value = getattr(obj, attr, "")
    if value:
        return "- " + value
    return ""
