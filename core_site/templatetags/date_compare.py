from datetime import datetime
from django import template

register = template.Library()

@register.filter
def date_compare(date1, date2=None):
    if date2 is None:
        date2 = datetime.now()
    difference = date2 - date1
    return difference.years