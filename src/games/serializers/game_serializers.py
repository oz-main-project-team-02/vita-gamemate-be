from rest_framework import serializers

from games.models.game_model import Game


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ["id", "name", "image"]
