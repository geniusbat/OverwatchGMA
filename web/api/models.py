from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    comment = models.CharField(verbose_name="Comment", max_length=86, default="", blank=True)