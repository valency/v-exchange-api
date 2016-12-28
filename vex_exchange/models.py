from django.db import models

TRADE_TYPE = (
    (1, "Buy"),
    (2, "Sell")
)


class Stock(models.Model):
    id = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=32)
    enabled = models.BooleanField(default=True)
    registered = models.DateTimeField()


class Holding(models.Model):
    account = models.ForeignKey("vex_auth.Account", related_name="+")
    stock = models.ForeignKey("vex_exchange.Stock", related_name="+")
    amount = models.IntegerField()


class Listing(models.Model):
    t = models.DateTimeField()
    stock = models.ForeignKey("vex_exchange.Stock", related_name="+")
    account = models.ForeignKey("vex_auth.Account", related_name="+")
    type = models.IntegerField(choices=TRADE_TYPE)
    price = models.FloatField()
    amount = models.IntegerField()


class Exchange(models.Model):
    t = models.DateTimeField()
    stock = models.ForeignKey("vex_exchange.Stock", related_name="+")
    account_a = models.ForeignKey("vex_auth.Account", related_name="+")
    account_b = models.ForeignKey("vex_auth.Account", related_name="+")
    type_a = models.IntegerField(choices=TRADE_TYPE)
    type_b = models.IntegerField(choices=TRADE_TYPE)
    price = models.FloatField()
    amount = models.IntegerField()
    total = models.FloatField()
