from rest_framework import serializers

from .models import PaymentConfig


class PaymentConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentConfig
        fields = ('amount', 'description')
