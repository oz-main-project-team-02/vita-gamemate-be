from rest_framework import serializers

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
