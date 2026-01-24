import binascii, os
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class UserData(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='data'
    )
    comment = models.CharField("comment", max_length=85,default="")

    class Meta():
        ordering = ["user"]
        verbose_name = "user data"
        verbose_name_plural = "users data"
    
    @property
    def last_login(self):
        return self.user.last_login
    @property
    def token(self):
        return self.user.auth_token
    
    def __str__(self):
        return str(self.user)

class DelegateToken(models.Model):
    """
    Auth key used for delegate hosts. Directly copied from the rest_framework.authtoken.models Token class
    """
    key = models.CharField("Key", max_length=40, primary_key=True)
    created = models.DateTimeField("Created", auto_now_add=True)

    class Meta:
        ordering = ["-created","hosts_registry"]
        verbose_name = "Delegate Token"
        verbose_name_plural = "Delegate Tokens"

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return self.key