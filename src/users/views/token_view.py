from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(TokenRefreshView):

    @extend_schema(
        methods=["POST"],
        summary="토큰 재발급",
        description="refresh_token을 이용한 access_token 재발급 API입니다. Body에서 값을 보내주세요.",
        responses={
            status.HTTP_200_OK: OpenApiTypes.OBJECT,
            status.HTTP_401_UNAUTHORIZED: OpenApiTypes.OBJECT,
        },
        examples=[
            OpenApiExample(
                "Valid Token 응답 예제",
                summary="유효한 토큰 응답 예제",
                description="토큰이 유효하다면 access_token 발급",
                value={
                    "refresh": "asdfasfdsadf1",
                },
                status_codes=[status.HTTP_200_OK],
            ),
            OpenApiExample(
                "Blacklist Token 응답 예제",
                summary="블랙 리스트된 토큰 응답 예제",
                description="로그아웃시 무효화 시킨 토큰입니다.",
                value={
                    "detail": "블랙리스트에 추가된 토큰입니다",
                    "code": "token_not_valid",
                },
                status_codes=[status.HTTP_401_UNAUTHORIZED],
            ),
            OpenApiExample(
                "Invalid Token 응답 예제",
                summary="유효하지 않은 토큰 응답 예제",
                description="유효하지 않은 토큰입니다.",
                value={
                    "detail": "유효하지 않거나 만료된 토큰입니다",
                    "code": "token_not_valid",
                },
                status_codes=[status.HTTP_401_UNAUTHORIZED],
            ),
        ],
    )
    def post(self, request: Request) -> Response:
        return super().post(request)
