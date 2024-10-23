from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from reviews.models import Review
from reviews.serializers.serializers import PaginatedReviewSerializer, ReviewSerializer
from reviews.utils import ReviewPagination


# 1. 특정 게임 의뢰에 대한 리뷰 조회
class GameRequestReviewListAPIView(APIView):
    pagination_class = ReviewPagination

    def get(self, request, game_request_id):

        reviews = Review.objects.filter(game_request_id=game_request_id).order_by("-created_at")

        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        serializer = PaginatedReviewSerializer(
            {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": ReviewSerializer(paginated_reviews, many=True).data,
            }
        )

        return Response(serializer.data)


# 2. 특정 사용자의 특정 게임 리뷰 조회
class UserGameReviewListAPIView(APIView):
    pagination_class = ReviewPagination

    def get(self, request, user_id, game_id):

        reviews = Review.objects.filter(game_request__user_id=user_id, game_request__game_id=game_id).order_by("-created_at")

        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)

        serializer = PaginatedReviewSerializer(
            {
                "count": paginator.page.paginator.count,
                "next": paginator.get_next_link(),
                "previous": paginator.get_previous_link(),
                "results": ReviewSerializer(paginated_reviews, many=True).data,
            }
        )

        return Response(serializer.data)


# 3. 특정 사용자의 전체 리뷰 조회
class UserReviewListAPIView(APIView):
    pagination_class = ReviewPagination

    def get(self, request, user_id):

        reviews = Review.objects.filter(game_request__user_id=user_id).order_by("-created_at")

        paginator = self.pagination_class()
        paginated_reviews = paginator.paginate_queryset(reviews, request)
        serializer = ReviewSerializer(paginated_reviews, many=True)
        response = paginator.get_paginated_response(serializer.data)
        print(response.data)

        return response
