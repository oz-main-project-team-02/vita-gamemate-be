from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
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
        self.redis_instance = await sync_to_async(get_redis_connection)("default")

        access_token = self.scope["query_string"].decode("utf-8").split("token=")[-1]

        try:
            self.user = await self.get_user_from_access_token(access_token)

            if not self.user.is_authenticated:
                await self.close()

        except (MissingAuthorizationHeader, InvalidAuthorizationHeader, TokenMissing, UserNotFound):
            await self.close()

        await self.update_user_status(self.user, True)

        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "user") and self.user.is_authenticated:
            await self.delete_user_status(self.user)

        await self.close()

    @sync_to_async
    def get_user_from_access_token(self, access_token):
        return UserService.get_user_from_access_token(access_token)

    @sync_to_async
    def update_user_status(self, user, status):
        self.redis_instance.set(f"user:{user.id}:is_online", str(status))

    @sync_to_async
    def delete_user_status(self, user):
        self.redis_instance.delete(f"user:{user.id}:is_online")
