from rest_framework import serializers


class TokenBlacklistSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
