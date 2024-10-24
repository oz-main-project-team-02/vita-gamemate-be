from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    payment_key = serializers.CharField(max_length=255)
    order_id = serializers.CharField(max_length=255)
    amount = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = ['payment_key', 'order_id', 'amount']
