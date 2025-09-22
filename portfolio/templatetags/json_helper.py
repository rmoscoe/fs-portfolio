from django import template
from django.core.serializers.json import DjangoJSONEncoder
import json

register = template.Library()

@register.filter
def json_helper(content, action='loads'):
    if action not in ('loads', 'dumps'):
        action = 'loads'
    
    try:
        match action:
            case 'loads':
                return json.loads(content)
            case 'dumps':
                return json.dumps(content, cls=DjangoJSONEncoder)
            case _:
                return content
    except Exception:
        return content