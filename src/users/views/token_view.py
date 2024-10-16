from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiTypes,
    extend_schema,
    OpenApiResponse,
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
        request={"application/json": {"type": "object", "properties": {"refresh": {"type": "string"}}, "required": ["refresh"]}},
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={"type": "object", "properties": {"access": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="유효한 토큰 응답",
                        value={"access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={"type": "object", "properties": {"detail": {"type": "string"}, "code": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="블랙리스트된 토큰",
                        value={"detail": "블랙리스트에 추가된 토큰입니다", "code": "token_not_valid"},
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="유효하지 않은 토큰",
                        value={"detail": "유효하지 않거나 만료된 토큰입니다", "code": "token_not_valid"},
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def post(self, request: Request) -> Response:
        return super().post(request)
