from rest_framework import serializers
from django.contrib.auth.models import User
from . import models


class Payment_Serializer(serializers.ModelSerializer):
    class Meta:
        model = models.Payment_Model
        fields = ['id', 'user', 'order', 'amount', 'transaction_id', 'payment_status', 'payment_time']