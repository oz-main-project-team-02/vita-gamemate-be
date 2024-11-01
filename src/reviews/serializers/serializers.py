from rest_framework import serializers

from game_requests.models import GameRequest
from reviews.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    game_request_id = serializers.IntegerField(source="game_request.id", read_only=True)
    game_id = serializers.IntegerField(source="game_request.game.id", read_only=True)
    author_id = serializers.SerializerMethodField()
    author_nickname = serializers.CharField(source="game_request.user.nickname", read_only=True)
    mate_nickname = serializers.CharField(source="game_request.mate.nickname", read_only=True)


    class Meta:
        model = Review
        fields = [
            "game_request_id",
            "game_id",
            "author_id",
            "author_nickname",
            "mate_nickname",
            "rating",
            "content",
            "created_at"
        ]

    def get_author_id(self, obj):
        return obj.game_request.user.id if obj.game_request and obj.game_request.user else None


class PaginatedReviewSerializer(serializers.Serializer):
    count = serializers.IntegerField()
    next = serializers.CharField(allow_null=True)
    previous = serializers.CharField(allow_null=True)
    results = ReviewSerializer(many=True)


class AllReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ["game_request", "rating", "content", "created_at"]

    def validate(self, data):
        request = self.context.get("request")
        user = request.user
        game_request = data["game_request"]

        # 게임 요청이 사용자와 연결되어 있는지 확인
        if game_request.user != user:
            raise serializers.ValidationError("본인이 의뢰한 게임에 대해서만 리뷰를 작성할 수 있습니다.")

        # 게임 요청이 완료 상태인지 확인
        if not game_request.status:
            raise serializers.ValidationError("완료되지 않은 게임 요청에 대해서는 리뷰를 작성할 수 없습니다.")

        # 이미 리뷰가 작성되었는지 확인
        if game_request.review_status:
            raise serializers.ValidationError("해당 게임 요청에 대한 리뷰는 이미 존재합니다.")

        return data

    def validate_rating(self, value):
        if value < 1.0 or value > 5.0:
            raise serializers.ValidationError("평점은 1.0에서 5.0 사이여야 합니다.")
        return value


class GameReviewSerializer(serializers.ModelSerializer):
    mate_id = serializers.IntegerField(source="game_request.mate_id", read_only=True)
    mate_nickname = serializers.CharField(source="game_request.mate.nickname", read_only=True)
    author_id = serializers.IntegerField(source="game_request.user.id", read_only=True)
    author_nickname = serializers.CharField(source="game_request.user.nickname", read_only=True)
    game_request_id = serializers.IntegerField(source="game_request.id", read_only=True)
    game_id = serializers.IntegerField(source="game_request.game.id", read_only=True)

    class Meta:
        model = Review
        fields = [
            "mate_id",
            "mate_nickname",
            "game_id",
            "game_request_id",
            "author_id",
            "author_nickname",
            "rating",
            "content",
            "created_at",
        ]
