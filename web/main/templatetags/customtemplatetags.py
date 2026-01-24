from django import template
import datetime

register = template.Library()

@register.filter
def secs_to_datetime(value):
    try:
        return datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S %d-%m-%Y")
    except:
        return None

@register.filter
def secs_to_time(value):
    try:
        if value < 0:
            return "0s"
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

@register.filter
def substract(first,second):
    try:
        return first-second
    except:
        return "Substraction didn't work"