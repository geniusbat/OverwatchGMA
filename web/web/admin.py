from django.contrib import admin
from django.utils.html import escape, mark_safe
from django.urls import reverse
from django.contrib.auth.admin import UserAdmin
from .models import User, UserData, DelegateToken, TokenLogs

class CustomUserAdmin(UserAdmin):
    list_display = ("username", "comment", "date_joined","is_staff", "last_login", "is_active")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "comment", "groups")
    ordering = ("is_active","username","-date_joined")

    def _link_to_data(self, obj, text):
        link = reverse(f"admin:web_userdata_change", args=[obj.data.pk])
        return mark_safe(f'<a href="{link}">{text}</a>')
    
    def comment(self, obj):
        return self._link_to_data(obj, obj.data.comment)
admin.site.register(User, CustomUserAdmin)

class UserDataAdmin(admin.ModelAdmin):
    list_display = ["user","link_to_user","comment","token","last_login"]
    def link_to_user(self, obj):
        link = reverse(f"admin:web_user_change", args=[obj.user.pk])
        return mark_safe(f'<a href="{link}">Modify User</a>')
admin.site.register(UserData, UserDataAdmin)

class DeletageTokenAdmin(admin.ModelAdmin):
    list_display = ["host","created","key"]
    #Set default value for key
    def get_form(self, request, obj=None, **kwargs):
        form = super(DeletageTokenAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['key'].initial = DelegateToken.generate_key()
        return form
    #Print host name
    def host(self,obj):
        return obj.hosts_registry.host
    host.short_description = 'Host'
    host.admin_order_field = 'host'
admin.site.register(DelegateToken,DeletageTokenAdmin)

class TokenLogsAdmin(admin.ModelAdmin):
    list_display = ("time", "token_type", "token","ip", "log",)
    list_filter = ("token_type",)
    search_fields = ("ip", "token", "log")
    ordering = ("-time",)
admin.site.register(TokenLogs, TokenLogsAdmin)