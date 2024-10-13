from django.http import HttpRequest, HttpResponse
from django.urls import path


# 임시 뷰 함수 입니다.
def dummy_view(request: HttpRequest, *args: tuple[str, ...], **kwargs: dict[str, str]) -> HttpResponse:
    return HttpResponse("This is a dummy view")


urlpatterns = [
    # 실시간 생생후기 나열 (?limit=숫자&sort=latest)
    path("", dummy_view, name="reviews"),
    # 리뷰 작성
    path("<int:game_request_id>/write/", dummy_view, name="review-write"),
    # 유저의 리뷰 리스트 (?limit=숫자&sort=latest)
    path("<str:user_id>/", dummy_view, name="review-list"),
]
