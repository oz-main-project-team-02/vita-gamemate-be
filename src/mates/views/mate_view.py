from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from mates.models import MateGameInfo
from users.exceptions import MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound
from mates.serializers.mate_serializer import RegisterMateSerializer, MateSerializer
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

        return Response({"message": "메이트 등록이 완료되었습니다."}, status=status.HTTP_201_CREATED)
