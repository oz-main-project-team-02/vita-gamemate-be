from rest_framework import serializers

from users.models import User


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["nickname", "description", "gender", "birthday", "profile_image"]
