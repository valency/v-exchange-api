from django.db import models


class Stock(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=16)
    enabled = models.BooleanField(default=True)
