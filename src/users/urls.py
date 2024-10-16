from django.http import HttpRequest, HttpResponse
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from users.views import oauth_view, token_view, user_view


# 임시 뷰 함수 입니다.
def dummy_view(request: HttpRequest, *args: tuple[str, ...], **kwargs: dict[str, str]) -> HttpResponse:
    return HttpResponse("This is a dummy view")


urlpatterns = [
    # 사용자 로그인 회원가입
    path("google/login/", oauth_view.GoogleLoginAPIView.as_view(), name="google-login"),
    path("google/login/callback/", oauth_view.GoogleLoginCallbackAPIView.as_view(), name="google-login-callback"),
    path("kakao/login/", oauth_view.KakaoLoginAPIView.as_view(), name="kakao-login"),
    path("kakao/login/callback/", oauth_view.KakaoLoginCallbackAPIView.as_view(), name="kakao-login-callback"),
    path("auth/logout/", oauth_view.LogoutAPIView.as_view(), name="auth-logout"),
    # access token 발금
    path("auth/accesstoken/", token_view.CustomTokenRefreshView.as_view(), name="auth-accesstoken"),
    # 사용자 프로필
    path("<int:user_id>/profile/", user_view.UserProfileAPIView.as_view(), name="user-profile"),
    # 내 프로필
    path("profile/me/", user_view.UserMeAPIView.as_view(), name="user-me"),
    # 게임 메이트 리스트
    # 게임 메이트 프로필 편집
    path("<str:user_id>/profile/gamemate/", dummy_view, name="gamemate-profile"),
    # 오늘의 게임 메이트 (몇명 보여줘야 할지는 요구사항에 적혀 있진 않음 일단 5명이고 랜덤으로, ?limit=5)
    path("gamemates/recommended/today/", dummy_view, name="gamemates-recommended"),
    # 게임 카테고리에 따른 메이트 추천 (?game=게임아이디&limit=숫자)
    path("gamemates/recommended/", dummy_view, name="gamemates-recommended"),
    # 사용자 리스트 (?game=게임아이디&sort=recommended,new,rating,low_price,high_price)
    # 그리고 (?game=게임아이디&gender=male,female)
    # 그리고 (?game=게임아이디&page=숫자)
    path("gamemates", dummy_view, name="gamemates-filter"),
]
