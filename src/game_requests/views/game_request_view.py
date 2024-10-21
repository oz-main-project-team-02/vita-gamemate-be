from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from game_requests.models import GameRequest
from game_requests.serializers.game_request_serializer import (
    GameRequestCreateSerializer,
    GameRequestOrderedSerializer,
    GameRequestReceivedSerializer,
)
from game_requests.utils import GameRequestPagination
from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models import User
from users.services.user_service import UserService


class GameRequestCreateAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, user_id):
        try:
            mate = User.objects.get(id=user_id, is_mate=True)
        except User.DoesNotExist:
            return Response({"error": "사용자를 찾지 못했습니다."}, status=status.HTTP_404_NOT_FOUND)

        authorization_header = request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"error": str(e)}, status=e.status_code)

        if user_id == user.id:
            return Response({"error": "자신에게 의뢰 할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GameRequestCreateSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        GameRequest.objects.create(user_id=user.id, mate_id=mate.id, **serializer.validated_data)

        return Response({"message": "의뢰가 접수 되었습니다."}, status=status.HTTP_201_CREATED)


class GameRequestOrderedAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = GameRequestPagination

    def get(self, request):
        authorization_header = request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"error": str(e)}, status=e.status_code)

        game_requests = GameRequest.objects.filter(user=user).order_by("-created_at")

        paginator = self.pagination_class()
        paginated_requests = paginator.paginate_queryset(game_requests, request)

        serializer = GameRequestOrderedSerializer(paginated_requests, many=True)

        return paginator.get_paginated_response(serializer.data)


class GameRequestReceivedAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    pagination_class = GameRequestPagination

    def get(self, request):
        authorization_header = request.headers.get("Authorization")

        try:
            mate = UserService.get_user_from_token(authorization_header)

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"error": str(e)}, status=e.status_code)

        game_requests = GameRequest.objects.filter(mate=mate).order_by("-created_at")

        paginator = self.pagination_class()
        paginated_requests = paginator.paginate_queryset(game_requests, request)

        serializer = GameRequestReceivedSerializer(paginated_requests, many=True)

        return paginator.get_paginated_response(serializer.data)
