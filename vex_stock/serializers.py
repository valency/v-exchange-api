from rest_framework import serializers

from vex_exchange.models import *


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
