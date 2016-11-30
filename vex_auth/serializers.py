from rest_framework import serializers

from vex_auth.models import *


class AccountSerializer(serializers.ModelSerializer):
    password = serializers.HiddenField(default=None)
    ticket = serializers.HiddenField(default=None)

    class Meta:
        model = Account
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = '__all__'
