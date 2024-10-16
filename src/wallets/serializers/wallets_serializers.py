from rest_framework import serializers


class WalletBalanceSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()

    def validate_user_id(self, value):
        request_user = self.context["request"].user
        if request_user.id != value:
            raise serializers.ValidationError("본인의 정보만 조회할 수 있습니다.")
        return value


class WalletRechargeSerializer(serializers.Serializer):
    coin = serializers.IntegerField(required=True)

    def validate(self, attrs):
        coin_amount = attrs.get("coin")
        # coin 값이 없는 경우나 유효하지 않은 경우를 처리
        if coin_amount is None:
            raise serializers.ValidationError({"coin": "충전할 코인 양을 입력해야 합니다."})

        if coin_amount <= 0:
            raise serializers.ValidationError({"coin": "충전할 코인 양은 1 이상이어야 합니다."})

        if coin_amount <= 0:
            raise serializers.ValidationError({"coin": "코인의 충전양은 0보다 커야합니다."})
        return attrs
