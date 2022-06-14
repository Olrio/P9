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

@register.simple_tag(takes_context=True)
def get_instance_user(context, user):
    if user == context['instance'].user:
        return 'Vous avez'
    return f"{context['instance'].user} a"

@register.simple_tag(takes_context=True)
def get_detail_instance_user(context, user, instance):
    if instance == "ticket":
        if user == context['ticket'].user:
            return 'Vous avez'
        return f"{context['ticket'].user} a"
    elif instance == "review":
        if user == context['review'].user:
            return 'Vous avez'
        return f"{context['review'].user} a"


@register.simple_tag(takes_context=True)
def get_ticket_author(context, user):
    if user == context['instance'].ticket.user:
        return 'Votre ticket'
    return f"Ticket de {context['instance'].ticket.user}"