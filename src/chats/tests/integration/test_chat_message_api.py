from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chats.models import ChatRoom, Message
from users.models import User


class ChatMessageAPITest(APITestCase):
    def setUp(self):
        self.main_user = User.objects.create_user(
            nickname="서강준",
            social_provider="google",
            email="haha@haha.com",
        )

        self.other_user = User.objects.create_user(
            nickname="아이유",
            social_provider="google",
            email="ee@ee.com",
        )
        self.chat_room = ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)
        self.list_messages_url = reverse("chat_messages", kwargs={"room_id": self.chat_room.id})

        self.token = str(TokenObtainPairSerializer.get_token(self.main_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_list_messages_success(self):
        Message.objects.create(room=self.chat_room, sender_nickname=self.main_user.nickname, text="하이!")

        response = self.client.get(self.list_messages_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_messages_room_not_found(self):
        response = self.client.get(reverse("chat_messages", kwargs={"room_id": 99}))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_messages_missing_room_id(self):
        response = self.client.get(self.list_messages_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
