from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from . import models

models.User._meta.app_label = "auth" #Change meta to add it to the correct app
admin.site.register(models.User, UserAdmin)