from django import template
import datetime

register = template.Library()

@register.filter
def secs_to_time(value):
    try:
        if value < 0:
            return "0 seconds"

        hours = int(value // 3600)
        minutes = int((value % 3600) // 60)
        value = int(value % 60)
        if hours > 0:
            return f"{hours}h {minutes}m {value}s"
        elif minutes > 0:
            return f"{minutes}m {value}s"
        else:
            return f"{value}s"
    except:
        return None
    
@register.filter
def acces_dict(value:dict,key):
    return value[key]
