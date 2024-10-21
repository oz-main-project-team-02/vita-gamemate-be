from django.urls import path

from game_requests.views.game_request_view import (
    GameRequestCreateAPIView,
    GameRequestOrderedAPIView,
    GameRequestReceivedAPIView,
)

urlpatterns = [
    path("<int:user_id>/", GameRequestCreateAPIView.as_view(), name="game-request"),
    path("ordered/", GameRequestOrderedAPIView.as_view(), name="ordered-game-request"),
    path("received/", GameRequestReceivedAPIView.as_view(), name="received-game-request"),
]
