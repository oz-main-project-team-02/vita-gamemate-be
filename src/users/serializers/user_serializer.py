from django_redis import get_redis_connection
from rest_framework import serializers

from mates.serializers.mate_serializer import MateGameInfoSerializer
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "email",
            "gender",
            "profile_image",
            "birthday",
            "description",
            "social_provider",
            "is_mate",
            "is_online",
        ]
        extra_kwargs = {
            "email": {"required": False},
        }

    def get_is_online(self, user):
        redis_instance = get_redis_connection("default")

        is_online = redis_instance.get(f"user:{user.id}:is_online")

        if not is_online:
            return False

        return is_online.decode("utf-8").lower() == "true"


class UserMateSerializer(serializers.ModelSerializer):
    mate_game_info = MateGameInfoSerializer(source="mategameinfo_set", many=True, read_only=True)
    is_online = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "nickname",
            "email",
            "gender",
            "profile_image",
            "birthday",
            "description",
            "social_provider",
            "is_mate",
            "is_online",
            "mate_game_info",
        ]

    def get_is_online(self, user):
        redis_instance = get_redis_connection("default")

        is_online = redis_instance.get(f"user:{user.id}:is_online")

        if not is_online:
            return False

        return is_online.decode("utf-8").lower() == "true"
