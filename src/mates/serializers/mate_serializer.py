from rest_framework import serializers

from games.models import Game
from mates.models import MateGameInfo


class RegisterMateSerializer(serializers.ModelSerializer):
    game_id = serializers.PrimaryKeyRelatedField(
        source="game",
        queryset=Game.objects.all(),
        write_only=True,
    )

    class Meta:
        model = MateGameInfo
        exclude = [
            "id",
            "user",
            "game",
            "updated_at",
            "created_at",
        ]


class MateGameInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = MateGameInfo
        fields = ["game_id", "description", "image", "level", "request_price"]
