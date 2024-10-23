from django.core.exceptions import ValidationError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from mates.exceptions import InvalidLevelError
from mates.models import MateGameInfo
from mates.serializers.mate_serializer import RegisterMateSerializer
from mates.utils import MateGameInfoPagination
from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models import User
from users.serializers.user_serializer import UserMateSerializer
from users.services.user_service import UserService


class RegisterMateAPIView(APIView):
    def post(self, request):
        authorization_header = request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"error": str(e)}, status=e.status_code)

        serializer = RegisterMateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            # serializer.errors 로 정확한 에러 출력

        try:
            MateGameInfo.objects.create(user_id=user.id, **serializer.validated_data)

        except ValidationError:
            return Response({"error": "이미 해당 게임이 등록 되어 있습니다."}, status=status.HTTP_400_BAD_REQUEST)

        except InvalidLevelError as e:
            return Response({"error": str(e)}, status=e.status_code)

        return Response({"message": "메이트 등록이 완료되었습니다."}, status=status.HTTP_201_CREATED)


class MateGameInfoListView(generics.ListAPIView):
    serializer_class = UserMateSerializer
    pagination_class = MateGameInfoPagination  # 페이지네이션 설정

    def get_queryset(self):
        game_id = self.kwargs.get("game_id")

        if game_id:
            queryset = User.objects.filter(mategameinfo__game_id=game_id)
        else:
            queryset = User.objects.filter(mategameinfo__isnull=False)

        gender = self.request.query_params.get("gender", "all")

        if gender in ["male", "female"]:
            queryset = queryset.filter(gender=gender)

        level = self.request.query_params.get("level")

        if level:
            level_list = level.split(",")
            queryset = queryset.filter(mategameinfo__level__in=level_list)

        # 정렬 처리
        sort = self.request.query_params.get("sort")

        if sort == "recommendation":
            queryset = queryset.order_by("-mategameinfo__created_at")  # 추천순 (필드 및 수정 필요)

        elif sort == "new":
            queryset = queryset.order_by("-mategameinfo__created_at")

        elif sort == "rating_desc":
            queryset = queryset.order_by("-mategameinfo__created_at")  # 평점순 (필드 및 수정 필요)

        elif sort == "price_asc":
            queryset = queryset.order_by("mategameinfo__request_price")

        elif sort == "price_desc":
            queryset = queryset.order_by("-mategameinfo__request_price")

        return queryset.distinct()
