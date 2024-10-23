from django.urls import path

from reviews.views.reviews_views import (
    GameRequestReviewListAPIView,
    UserGameReviewListAPIView,
    UserReviewListAPIView,
)

urlpatterns = [
    # 해당하는 게임 의뢰의 리뷰 조회, 한 페이지당 10개의 데이터
    path("<int:game_request_id>/", GameRequestReviewListAPIView.as_view(), name="reviews-request"),
    # 해당하는 사용자의 게임별 리뷰 목록 조회, 한 페이지당 10개의 데이터
    path("<int:user_id>/<int:game_id>/", UserGameReviewListAPIView.as_view(), name="review-game"),
    # 해당하는 사용자의 전체 리뷰 목록 조회, 한 페이지당 10개의 데이터
    path("<int:user_id>/", UserReviewListAPIView.as_view(), name="review-list"),
]

