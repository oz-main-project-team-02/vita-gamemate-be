from rest_framework import serializers

from mates.serializers.mate_serializer import MateGameInfoSerializer
from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = [
            "password",
            "is_active",
            "is_superuser",
            "is_staff",
            "last_login",
            "updated_at",
            "created_at",
            "groups",
            "user_permissions",
        ]
        extra_kwargs = {
            "email": {"required": False},
        }


class UserMateSerializer(serializers.ModelSerializer):
    mate_game_info = MateGameInfoSerializer(source="mategameinfo_set", many=True, read_only=True)

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
            "is_online",
            "is_mate",
            "mate_game_info",
        ]
