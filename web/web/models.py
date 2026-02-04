import binascii, os
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token
import datetime

def _aux_get_now_utc_timestamp():
    return int(datetime.datetime.now(datetime.UTC).timestamp())

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

class TokenLogs(models.Model):
    """
    Class to store access/action logs of DRF Tokens and DelegateTokens
    """
    time = models.DateTimeField("log time", default=_aux_get_now_utc_timestamp, editable=False)
    token_type = models.CharField("token type", max_length=15)
    token = models.CharField("token used", max_length=40) #We store the token as string as it can be either from DRF's tokens or DelegateTokens
    ip = models.CharField(max_length=39, blank=True, default="")
    log = models.TextField("log")

    class Meta():
        ordering = ["-time"]
        verbose_name = "Token log"
        verbose_name_plural = "Tokens logs"

    #TODO: Check that tokens come from similar ips if not raise alarm --> Match tokens to ips so if attacker grabs a token then i am warned