from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView


class CustomTokenRefreshView(APIView):

    @extend_schema(
        methods=["GET"],
        tags=["auth"],
        summary="토큰 재발급",
        auth=[],
        description="refresh_token을 이용한 access_token 재발급 API입니다. 스웨거에서는 직접 쿠키 값을 입력하지 못합니다. 브라우저에 쿠키 값에 refresh token이 있다면 그 값을 가져옵니다.",
        request=None,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response={"type": "object", "properties": {"access": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="유효한 토큰 응답",
                        value={"access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={"type": "object", "properties": {"detail": {"type": "string"}, "code": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="토큰 에러",
                        value={
                            "error": "유효하지 않거나 만료된 토큰입니다.",
                        },
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def get(self, request: Request) -> Response:
        refresh_token = request.COOKIES.get("refresh_token")  # 쿠키에서 refresh 토큰 가져오기

        if not refresh_token:
            return Response({"detail": "refresh token이 쿠키에 존재하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            return Response({"access_token": access_token}, status=status.HTTP_200_OK)

        except TokenError as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)
