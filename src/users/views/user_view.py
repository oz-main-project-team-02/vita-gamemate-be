from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from users.models import User
from users.serializers.user_serializer import UserProfileSerializer
from users.services.user_service import UserService


class UserProfileAPIView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    @extend_schema(
        methods=["GET"],
        tags=["user"],
        auth=[],
        summary="사용자 프로필 정보 가져오기",
        description="gender, description, profile_image, birth는 null값과 str을 반환할 수 있음.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                examples=[
                    OpenApiExample(
                        name="사용자 정보 가져옴",
                        value={
                            "id": 200,
                            "nickname": "fake0",
                            "email": "fakeuser0@user.com",
                            "gender": None,
                            "profile_image": None,
                            "birthday": None,
                            "description": None,
                            "social_provider": "kakao",
                            "is_online": True,
                            "is_mate": False,
                        },
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="사용자를 찾지 못함",
                        value={"message": "사용자를 찾지 못했습니다."},
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def get(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user)  # 사용자가 보낸 데이터는 아니기 때문에 validation은 할 필요 없다고 생각함

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMeAPIView(APIView):
    serializer_class = UserProfileSerializer

    @extend_schema(
        methods=["GET"],
        tags=["user"],
        summary="내 프로필 정보 가져오기",
        description="gender, description, profile_image, birth는 null값과 str을 반환할 수 있음. 오른쪽 자물쇠에 access token 입력.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                examples=[
                    OpenApiExample(
                        name="프로필 정보 조회 성공",
                        value={
                            "id": 200,
                            "nickname": "fake0",
                            "email": "fakeuser0@user.com",
                            "gender": None,
                            "profile_image": None,
                            "birthday": None,
                            "description": None,
                            "social_provider": "kakao",
                            "is_online": True,
                            "is_mate": False,
                        },
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="잘못된 토큰",
                        value={"message": "토큰이 유효하지 않습니다."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="토큰 누락",
                        value={"message": "access_token을 가져오지 못했습니다."},
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="사용자 없음",
                        value={"message": "사용자를 찾지 못했습니다."},
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def get(self, request):
        authorization_header = request.headers.get("Authorization")
        user, response = UserService.get_user_from_token(authorization_header)

        if response:
            return response

        serializer = UserProfileSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        methods=["PATCH"],
        tags=["user"],
        summary="내 프로필 정보 수정하기",
        description="header에 Authorization: Bearer your_access_token 필수",
        request=UserProfileSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                examples=[
                    OpenApiExample(
                        name="성공",
                        value={
                            "id": 200,
                            "nickname": "fake0",
                            "email": "fakeuser0@user.com",
                            "gender": None,
                            "profile_image": None,
                            "birthday": None,
                            "description": None,
                            "social_provider": "kakao",
                            "is_online": True,
                            "is_mate": False,
                        },
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="유효하지 않은 Authorization 헤더",
                        value={"message": "유효하지 않은 Authorization 헤더입니다."},
                        response_only=True,
                    ),
                    OpenApiExample(
                        name="Authorization 헤더 누락",
                        value={"message": "Authorization 헤더가 누락되었습니다."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="유효하지 않은 토큰",
                        value={"message": "토큰이 유효하지 않습니다."},
                        response_only=True,
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response={"type": "object", "properties": {"message": {"type": "string"}}},
                examples=[
                    OpenApiExample(
                        name="사용자를 찾지 못함",
                        value={"message": "사용자를 찾지 못했습니다."},
                        response_only=True,
                    ),
                ],
            ),
        },
    )
    def patch(self, request):
        authorization_header = request.headers.get("Authorization")
        user, response = UserService.get_user_from_token(authorization_header)

        if response:
            return response

        serializer = UserProfileSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)