from django.urls import path

from users.views import oauth_view, token_view, user_view

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
]
