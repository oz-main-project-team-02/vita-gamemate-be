from django.http import HttpRequest, HttpResponse
from django.urls import path

from games.views.game_view import GameDetailView, GameListView, PopularGameListView


# 임시 뷰 함수 입니다.
def dummy_view(request: HttpRequest, *args: tuple[str, ...], **kwargs: dict[str, str]) -> HttpResponse:
    return HttpResponse("This is a dummy view")


urlpatterns = [
    # 게임 목록 (?limit=숫자&sort=nav(nav bar 용), best(인기순))
    path("", GameListView.as_view(), name="game-list"),
    path("<int:game_id>/", GameDetailView.as_view(), name="game-detail"),
    # 특정 게임 조회
    path("recommend/", PopularGameListView.as_view(), name="popular-games"),
    # 인기 게임 조회
    # 유저 자신의 신청한 의뢰 목록 (페이지네이션)
    path("<str:user_id>/game-requests/ordered/", dummy_view, name="ordered-game-requests"),
    # 유저 자신이 받은 외뢰 목록 (페이지네이션)
    path("<str:user_id>/game-requests/received/", dummy_view, name="received-game-requests"),
]
