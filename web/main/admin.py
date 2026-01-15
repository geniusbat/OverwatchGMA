from django.contrib import admin

from . import models

# Register your models here
class delegate_controlsAdmin(admin.ModelAdmin):
  ordering = ('-timestamp',)
  list_display = [field.name for field in models.delegate_controls._meta.get_fields()]
admin.site.register(models.delegate_controls,delegate_controlsAdmin)
class delegate_errorsAdmin(admin.ModelAdmin):
  ordering = ('-timestamp',)
  list_display = [field.name for field in models.delegate_errors._meta.get_fields()]
admin.site.register(models.delegate_errors)
class hosts_registryAdmin(admin.ModelAdmin):
  ordering = ('-timestamp',)
  list_display = [field.name for field in models.hosts_registry._meta.get_fields()]
admin.site.register(models.hosts_registry)
class master_controlsAdmin(admin.ModelAdmin):
  ordering = ('-timestamp',)
  list_display = [field.name for field in models.master_controls._meta.get_fields()]
admin.site.register(models.master_controls)
class master_errorsAdmin(admin.ModelAdmin):
  ordering = ('-timestamp',)
  list_display = [field.name for field in models.master_errors._meta.get_fields()]
admin.site.register(models.master_errors)
