from rest_framework import serializers


class WalletRechargeSerializer(serializers.Serializer):
    coin = serializers.IntegerField(required=True)

    def validate(self, attrs):
        coin_amount = attrs.get("coin")

        if coin_amount is None:
            raise serializers.ValidationError({"coin": "충전할 코인 양을 입력해야 합니다."})

        if coin_amount <= 0:
            raise serializers.ValidationError({"coin": "충전할 코인 양은 1 이상이어야 합니다."})

        return attrs
