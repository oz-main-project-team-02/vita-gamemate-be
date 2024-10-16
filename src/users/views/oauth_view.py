from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenBlacklistSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from config.settings import GOOGLE_CONFIG, KAKAO_CONFIG
from users.models import User
from users.services.social_login_service import (
    SocialLoginCallbackService,
    SocialLoginService,
)


class GoogleLoginAPIView(APIView):
    permission_classes = [AllowAny]

    gl = SocialLoginService()

    gl.login_uri = GOOGLE_CONFIG["LOGIN_URI"]
    gl.client_id = GOOGLE_CONFIG["CLIENT_ID"]
    gl.redirect_uri = GOOGLE_CONFIG["REDIRECT_URI"]

    scope = GOOGLE_CONFIG["SCOPE"]

    @extend_schema(
        methods=["GET"],
        summary="구글 로그인 이동",
        description="swagger로는 작동하지 않습니다. 직접 url을 입력해보세요.",
    )
    def get(self, request):
        return redirect(self.gl.social_login(context={"scope": self.scope}))


class GoogleLoginCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    glc = SocialLoginCallbackService()

    glc.client_id = GOOGLE_CONFIG["CLIENT_ID"]
    glc.client_secret = GOOGLE_CONFIG["CLIENT_SECRET"]
    glc.token_uri = GOOGLE_CONFIG["TOKEN_URI"]
    glc.profile_uri = GOOGLE_CONFIG["PROFILE_URI"]
    glc.redirect_uri = GOOGLE_CONFIG["REDIRECT_URI"]

    @extend_schema(
        methods=["POST"],
        summary="구글 회원가입 / 로그인",
        description="자동으로 로그인 및 회원가입이되어 응답을 반환하는 API 입니다. google login url에서 자동으로 리다이렉트 되는 api입니다. swagger로 테스트 못합니다.",
        responses={
            status.HTTP_200_OK: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Successful Login",
                value={
                    "id": 1,
                    "email": "asdf@google.com",
                    "nickname": "asdf",
                    "social_provider": "google",
                    "gender": None,
                    "access_token": "asdfsadf",
                    "refresh_token": "asdfasdf",
                },
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def post(self, request):
        token_request_data = self.glc.create_token_request_data(code=request.data.get("code", None))
        auth_headers = self.glc.get_auth_headers(token_request_data=token_request_data)
        user_data = self.glc.get_user_info(auth_headers=auth_headers)

        email = user_data["email"]
        nickname = user_data["name"]
        social_provider = "google"

        try:
            user = User.objects.get(email=email, social_provider=social_provider)

        except ObjectDoesNotExist:
            user = User.objects.create_user(email=email, nickname=nickname, social_provider=social_provider)

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        data = {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
            "social_provider": social_provider,
            "gender": user.gender,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return Response(data, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        methods=["POST"],
        summary="로그아웃 (refresh_token 무효화)",
        description="refresh_token을 무효화 처리합니다.",
        request={
            "application/json": {"type": "object", "properties": {"refresh_token": {"type": "string"}}, "required": ["refresh_token"]}
        },
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="성공",
                        value={"message": "성공적으로 로그아웃 되었습니다."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object", "properties": {"error": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="토큰 누락",
                        value={"error": "refresh token이 없습니다."},
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response({"error": "refresh token이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "성공적으로 로그아웃 되었습니다."}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Unexpected Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class KakaoLoginAPIView(APIView):
    permission_classes = [AllowAny]

    kl = SocialLoginService()

    kl.login_uri = KAKAO_CONFIG["LOGIN_URI"]
    kl.client_id = KAKAO_CONFIG["REST_API_KEY"]
    kl.redirect_uri = KAKAO_CONFIG["REDIRECT_URI"]

    @extend_schema(
        methods=["GET"],
        summary="카카오 로그인 이동",
        description="swagger로는 작동하지 않습니다. 직접 url을 입력해보세요.",
    )
    def get(self, request):
        return redirect(self.kl.social_login())


class KakaoLoginCallbackAPIView(APIView):
    permission_classes = [AllowAny]

    klc = SocialLoginCallbackService()

    klc.client_id = KAKAO_CONFIG["REST_API_KEY"]
    klc.client_secret = KAKAO_CONFIG["CLIENT_SECRET_KEY"]
    klc.token_uri = KAKAO_CONFIG["TOKEN_URI"]
    klc.profile_uri = KAKAO_CONFIG["PROFILE_URI"]
    klc.redirect_uri = KAKAO_CONFIG["REDIRECT_URI"]

    @extend_schema(
        methods=["POST"],
        summary="카카오 회원가입 / 로그인",
        description="자동으로 로그인 및 회원가입이되어 응답을 반환하는 API 입니다. google login url에서 자동으로 리다이렉트 되는 api입니다. swagger로 테스트 못합니다.",
        responses={
            status.HTTP_200_OK: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Successful Login",
                value={
                    "id": 1,
                    "email": "asdf@kakao.com",
                    "nickname": "asdf",
                    "social_provider": "kakao",
                    "gender": None,
                    "access_token": "asdfsadf",
                    "refresh_token": "asdfasdf",
                },
                response_only=True,
                status_codes=[200],
            )
        ],
    )
    def post(self, request):
        token_request_data = self.klc.create_token_request_data(code=request.data.get("code", None))
        try:
            auth_headers = self.klc.get_auth_headers(token_request_data=token_request_data)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user_data = self.klc.get_user_info(auth_headers=auth_headers)

        profile_data = user_data["kakao_account"]["profile"]
        nickname = profile_data["nickname"]

        email = user_data["kakao_account"]["email"]
        social_provider = "kakao"

        try:
            user = User.objects.get(email=email, social_provider=social_provider)

        except ObjectDoesNotExist:
            user = User.objects.create_user(email=email, nickname=nickname, social_provider=social_provider)

        token = TokenObtainPairSerializer.get_token(user)
        access_token = str(token.access_token)
        refresh_token = str(token)

        data = {
            "id": user.id,
            "email": user.email,
            "nickname": user.nickname,
            "social_provider": social_provider,
            "gender": user.gender,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

        return Response(data, status=status.HTTP_200_OK)
