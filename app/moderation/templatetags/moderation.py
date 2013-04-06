from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import FlagType

register = template.Library()

@register.inclusion_tag('moderation/flag_form.html')
def flag_form(obj):
    return {
        'flagtypes': FlagType.objects.filter(is_active=True),
        'object': obj,
        'contenttype': ContentType.objects.get_for_model(obj),
    }


@register.inclusion_tag('moderation/flag_button.html')
def flag_button():
    return {}