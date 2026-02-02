from django.contrib import admin
from django.urls import reverse
from django.utils.html import escape, mark_safe

from . import models

import datetime

class TimestampFilter(admin.SimpleListFilter):
    title = 'Timestamp'
    parameter_name = 'timestamp_filter'

    def lookups(self, request, model_admin):
        return [
            ('15min', '15min'),
            ('1h', '1h'),
            ('1d', '1d'),
            ('7d', '7d'),
            ('1month', '1month')
        ]
    
    def queryset(self, request, queryset):
        time = datetime.datetime.now(datetime.UTC)
        if self.value() == "15min":
            time = time-datetime.timedelta(minutes=15)
        elif self.value() == "1h":
            time = time-datetime.timedelta(hours=1)
        elif self.value() == "1d":
            time = time-datetime.timedelta(days=1)
        elif self.value() == "7d":
            time = time-datetime.timedelta(days=7)
        elif self.value() == "1month":
            time = time-datetime.timedelta(days=30)
        else:
           return queryset
        return queryset.filter(timestamp__gte=time.timestamp())
   
class ReturncodeFilter(admin.FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        self.title = 'Returncode'
        # Define your lookup parameter
        self.lookup_kwarg = "returncode"
        self.lookup_choices = self.get_lookups(request)
        

    def get_lookups(self, request):
        return [
            ('any', 'All'),
            ('0', 'Ok'),
            ('1', 'No Good')
        ]

    def expected_parameters(self):
        return ["returncode"]

    def queryset(self, request, queryset):
        value = request.GET.get(self.lookup_kwarg)
        if value == "0":
            return queryset.filter(returncode=0)
        elif value == "1":
            return queryset.filter(returncode__gt=0)
        else:
           return queryset

    def choices(self, changelist):
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.lookup_kwarg == lookup,
                'query_string': changelist.get_query_string(
                    {self.lookup_kwarg: lookup} if lookup else {}
                ),
                'display': title,
            }


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

# Register your models here
class delegate_controlsAdmin(admin.ModelAdmin):
    list_display = ["host", "command_name", "time", "returncode", "message", "last_change_time"]
    list_filter = ["host", ("returncode",ReturncodeFilter), TimestampFilter]
    search_fields = ["command_name", "message", "previous_message"]
admin.site.register(models.delegate_controls,delegate_controlsAdmin)


class delegate_errorsAdmin(admin.ModelAdmin):
    list_display = ["host", "command_name", "time", "returncode", "message"]
    list_filter = ["host", ("returncode",ReturncodeFilter), TimestampFilter]
    search_fields = ["command_name", "message"]
admin.site.register(models.delegate_errors,delegate_errorsAdmin)


class hosts_registryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in models.hosts_registry._meta.get_fields()]
    list_display = list_display[:-1]
    list_display.append("link_to_token")
    list_filter = ["host"]
    search_fields = ["host", "ip", "valid_ips"]
    def link_to_token(self, obj):
        link = reverse(f"admin:web_delegatetoken_change", args=[obj.token.pk])
        return mark_safe(f'<a href="{link}">{escape(obj.token)}</a>')
    link_to_token.short_description = 'Token'
admin.site.register(models.hosts_registry,hosts_registryAdmin)


class master_controlsAdmin(admin.ModelAdmin):
    list_display = ["host", "command_name", "time", "returncode", "message"]
    list_filter = ["host", ("returncode",ReturncodeFilter), TimestampFilter]
    search_fields = ["command_name", "message"]
admin.site.register(models.master_controls,master_controlsAdmin)


class master_errorsAdmin(admin.ModelAdmin):
    list_display = ["host", "command_name", "time", "returncode", "message"]
    list_filter = ["host", ("returncode",ReturncodeFilter), TimestampFilter]
    search_fields = ["command_name", "message"]
admin.site.register(models.master_errors,master_errorsAdmin)