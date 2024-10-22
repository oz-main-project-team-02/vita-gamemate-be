from django.urls import path

from games.views.game_view import GameDetailView, GameListView, PopularGameListView

urlpatterns = [
    path("", GameListView.as_view(), name="game-list"),
    path("<int:game_id>/", GameDetailView.as_view(), name="game-detail"),
    path("recommend/", PopularGameListView.as_view(), name="popular-games"),
]
