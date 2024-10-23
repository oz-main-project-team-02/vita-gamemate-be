from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from chats.models import ChatRoom
from users.models import User


class ChatRoomAPITest(APITestCase):
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

        self.chat_room_create_url = reverse("chat_room_create")
        self.list_chat_rooms_url = reverse("chat_rooms")

        self.token = str(TokenObtainPairSerializer.get_token(self.main_user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_chat_room_success(self):
        response = self.client.post(self.chat_room_create_url, {"other_user_nickname": self.other_user.nickname})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatRoom.objects.count(), 1)

    def test_create_chat_room_existing(self):
        ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)

        response = self.client.post(self.chat_room_create_url, {"other_user_nickname": self.other_user.nickname})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChatRoom.objects.count(), 1)

    def test_create_chat_room_missing_nickname(self):
        """
        views.py에 36번째 줄 에서의 raise ValidationError 작동 하지 않고
        IsAuthenticated에서 먼저 validation 진행하여 error raise 해서 테스트 코드로 테스트 못함
        """
        response = self.client.post(self.chat_room_create_url, {"other_user_nickname": ""})

        # with self.assertRaises(ValidationError):
        #     response = self.client.post(self.chat_room_create_url, {"other_user_nickname": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_chat_rooms_success(self):
        ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)

        response = self.client.get(self.list_chat_rooms_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
