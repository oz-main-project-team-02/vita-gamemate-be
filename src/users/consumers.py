from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from django_redis import get_redis_connection

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.services.user_service import UserService


class StatusConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        headers = dict(self.scope["headers"])
        authorization_header = headers.get(b"authorization")

        if authorization_header:
            authorization_header = authorization_header.decode("utf-8")

        if not authorization_header:
            await self.close()

        try:
            self.user = await self.get_user_from_token(authorization_header)

            if not self.user.is_authenticated:
                await self.close()

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound):
            await self.close()

        await self.update_user_status(self.user, True)

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "user") and self.user.is_authenticated:
            await self.update_user_status(self.user, False)

        await self.close()

    @sync_to_async
    def get_user_from_token(self, token):
        return UserService.get_user_from_token(token)

    @sync_to_async
    def update_user_status(self, user, status):
        redis_instance = get_redis_connection("default")

        redis_instance.set(f"user:{user.id}:is_online", str(status))
