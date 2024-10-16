from django.http import HttpRequest, HttpResponse
from django.urls import path

from wallets.views.wallet_view import WalletBalanceView, WalletRechargeView

# 임시 뷰 함수 입니다.
# def dummy_view(request: HttpRequest, *args: tuple[str, ...], **kwargs: dict[str, str]) -> HttpResponse:
#     return HttpResponse("This is a dummy view")


urlpatterns = [
    # 나의 지갑 (코인 갯수)
    path("<int:user_id>/coin/", WalletBalanceView.as_view(), name="user-coin-wallet"),
    # 코인 충전
    path("<int:user_id>/coin/recharge/", WalletRechargeView.as_view(), name="user-coin-recharge"),
]
