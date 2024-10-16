from rest_framework import serializers

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
