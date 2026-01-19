from django.contrib import admin

from . import models

# Register your models here
class delegate_controlsAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.delegate_controls._meta.get_fields()]
admin.site.register(models.delegate_controls,delegate_controlsAdmin)


class delegate_errorsAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.delegate_errors._meta.get_fields()]
admin.site.register(models.delegate_errors,delegate_errorsAdmin)


class hosts_registryAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.hosts_registry._meta.get_fields()]
admin.site.register(models.hosts_registry,hosts_registryAdmin)


class master_controlsAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.master_controls._meta.get_fields()]
admin.site.register(models.master_controls,master_controlsAdmin)


class master_errorsAdmin(admin.ModelAdmin):
  list_display = [field.name for field in models.master_errors._meta.get_fields()]
admin.site.register(models.master_errors,master_errorsAdmin)
