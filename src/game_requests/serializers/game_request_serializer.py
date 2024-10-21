from rest_framework import serializers
from game_requests.models import GameRequest
from games.models import Game


class GameRequestCreateSerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(
        source="game",
        queryset=Game.objects.all(),
    )

    class Meta:
        model = GameRequest
        fields = ["game_id", "price", "amount"]


class GameRequestOrderedSerializer(serializers.ModelSerializer):
    game_request_id = serializers.IntegerField(source="id")
    mate_nickname = serializers.CharField(source="mate.nickname")
    mate_profile_image = serializers.ImageField(source="mate.profile_image")
    mate_gender = serializers.CharField(source="mate.gender")
    mate_online = serializers.BooleanField(source="mate.is_online")
    status = serializers.BooleanField()
    request_date = serializers.DateTimeField(source="created_at")
    request_amount = serializers.IntegerField(source="amount")

    class Meta:
        model = GameRequest
        fields = [
            "game_request_id",
            "mate_nickname",
            "mate_profile_image",
            "mate_gender",
            "mate_online",
            "status",
            "request_date",
            "request_amount",
        ]


class GameRequestReceivedSerializer(serializers.ModelSerializer):
    game_request_id = serializers.IntegerField(source="id")
    user_nickname = serializers.CharField(source="user.nickname")
    user_profile_image = serializers.ImageField(source="user.profile_image")
    user_gender = serializers.CharField(source="user.gender")
    user_online = serializers.BooleanField(source="user.is_online")
    status = serializers.BooleanField()
    request_date = serializers.DateTimeField(source="created_at")
    request_amount = serializers.IntegerField(source="amount")

    class Meta:
        model = GameRequest
        fields = [
            "game_request_id",
            "user_nickname",
            "user_profile_image",
            "user_gender",
            "user_online",
            "status",
            "request_date",
            "request_amount",
        ]
