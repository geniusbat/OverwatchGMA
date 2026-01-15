from django.contrib import admin

from . import models

# Register your models here.
admin.register(models.delegate_controls)
admin.register(models.delegate_errors)
admin.register(models.hosts_registry)
admin.register(models.master_controls)
admin.register(models.master_errors)
