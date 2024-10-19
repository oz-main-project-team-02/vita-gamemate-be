from django.conf import settings
from django.http import Http404, JsonResponse
from rest_framework import generics, serializers, status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.managers import UserManager
from users.services.user_service import UserService

from .models import ChatRoom, Message
from .serializers import ChatRoomSerializer, MessageSerializer


def perform_create(self, serializer):
    other_user_nickname = self.request.data.get("other_user_nickname")
    if not other_user_nickname:
        raise ValidationError("other_user_nickname 파라미터가 필요합니다.")

    main_user = self.get_user_from_request()
    other_user, _ = UserManager.get_user_by_nickname(other_user_nickname)

    existing_chatroom = ChatRoom.objects.filter(main_user=main_user, other_user=other_user).first()

    if existing_chatroom:
        serializer = self.get_serializer(existing_chatroom)
        response_data = serializer.data
        response_data["room_id"] = existing_chatroom.id
        return Response(response_data, status=status.HTTP_200_OK)

    chatroom = serializer.save(main_user=main_user, other_user=other_user)
    response_data = serializer.data
    response_data["room_id"] = chatroom.id
    return Response(response_data, status=status.HTTP_201_CREATED)


class ChatRoomListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def get_queryset(self):
        authorization_header = self.request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)
        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"message": str(e)}, status=e.status_code)

        return ChatRoom.objects.filter(main_user=user).order_by("-updated_at")


class MessageListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MessageSerializer

    def get_queryset(self):
        authorization_header = self.request.headers.get("Authorization")

        try:
            user = UserService.get_user_from_token(authorization_header)
        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound) as e:
            return Response({"message": str(e)}, status=e.status_code)

        room_id = self.kwargs.get("room_id")

        if not room_id:
            content = {"detail": "room_id 파라미터가 필요합니다."}
            raise ValidationError(content)

        queryset = Message.objects.filter(room_id=room_id)

        if not queryset.exists():
            raise Http404("해당 room_id로 메시지를 찾을 수 없습니다.")

        return queryset
