from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, extend_schema, OpenApiResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User
from users.serializers.user_serializer import UserProfileSerializer

# users = []
#
# for i in range(100, 200):
#     User.objects.create_user(
#         email=f"fakeuser{i}@user.com",
#         social_provider="google",
#         gender="male",
#         nickname=f"fake{i}",
#     ) or bulk create 해도 됩니다 하지만 bulk create는 비밀번호가 저장이 안돼요!


class UserProfileView(APIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    @extend_schema(
        methods=["GET"],
        summary="사용자 프로필 정보 가져오기",
        description="gender, description, profile_image, birth는 null값과 str을 반환할 수 있음",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                examples=[
                    OpenApiExample(
                        name="사용자 정보 가져옴",
                        value={
                            "nickname": "fake30",
                            "description": None,
                            "gender": "female",
                            "birthday": None,
                            "profile_image": None,
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

    @extend_schema(
        methods=["PATCH"],
        summary="사용자 프로필 정보 수정하기",
        description="gender, description, profile_image는 null값과 str을 반환할 수 있음",
        request=UserProfileSerializer,
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=UserProfileSerializer,
                examples=[
                    OpenApiExample(
                        name="성공",
                        value={
                            "nickname": "fake30",
                            "description": None,
                            "gender": "female",
                            "birthday": None,
                            "profile_image": None,
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
    def patch(self, request, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({"message": "사용자를 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
