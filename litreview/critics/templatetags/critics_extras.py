from django import template

register = template.Library()

@register.filter
def model_type(instance):
    return type(instance).__name__

@register.filter
def starring(instance):
    return "x"*instance.rating

@register.filter
def antistarring(instance):
    return "x"*(5-instance.rating)