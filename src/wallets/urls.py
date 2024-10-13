from django.http import HttpRequest, HttpResponse
from django.urls import path


# 임시 뷰 함수 입니다.
def dummy_view(request: HttpRequest, *args: tuple[str, ...], **kwargs: dict[str, str]) -> HttpResponse:
    return HttpResponse("This is a dummy view")


urlpatterns = [
    # 나의 지갑 (코인 갯수)
    path("<str:user_id>/coin/", dummy_view, name="user-coin-wallet"),
    # 코인 충전
    path("<str:user_id>/coin/recharge/", dummy_view, name="user-coin-recharge"),
]
