from django.contrib.postgres.fields import JSONField
from django.db import models

USER_GROUP = (
    (0, "User"),
    (1, "Admin")
)


class Account(models.Model):
    username = models.CharField(primary_key=True, max_length=16)
    password = models.CharField(max_length=128)
    ticket = models.CharField(max_length=36, null=True)
    last_login = models.DateTimeField(null=True)
    last_update = models.DateTimeField(null=True)
    register_time = models.DateTimeField(null=True)
    group = models.IntegerField(choices=USER_GROUP, default=0)
    ip = models.GenericIPAddressField(null=True)
    email = models.CharField(max_length=128, null=True)
    banned = models.BooleanField(default=False)
    balance = models.FloatField(default=0)
    balance_frozen = models.FloatField(default=0)


class Log(models.Model):
    account = models.ForeignKey("vex_auth.Account", on_delete=models.CASCADE, null=True)
    t = models.DateTimeField()
    type = models.CharField(max_length=128)
    ip = models.GenericIPAddressField(null=True)
    request = JSONField(null=True)
    response = JSONField(null=True)
