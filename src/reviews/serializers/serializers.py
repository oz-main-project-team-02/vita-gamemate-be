from rest_framework import serializers

from game_requests.models import GameRequest
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    game_request_id = serializers.IntegerField(source="game_request.id", read_only=True)

    class Meta:
        model = Review
        fields = ["game_request_id", "rating", "content", "created_at"]


class PaginatedReviewSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = ReviewSerializer(many=True)


class AllReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["game_request", "rating", "content", "created_at"]

    def validate_rating(self, value):
        if value < 1.0 or value > 5.0:
            raise serializers.ValidationError("평점은 1.0에서 5.0 사이여야 합니다.")
        return value
