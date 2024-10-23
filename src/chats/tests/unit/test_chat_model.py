from django.test import TestCase

from chats.models import ChatRoom, Message
from users.models import User


class ChatRoomModelTest(TestCase):
    def setUp(self):
        self.main_user = User.objects.create_user(nickname="하하", social_provider="google", email="haha@haha.com")
        self.other_user = User.objects.create_user(nickname="이이", social_provider="google", email="ee@ee.com")
        self.chat_room = ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)

    def test_chat_room_creation(self):
        self.assertEqual(self.chat_room.main_user, self.main_user)
        self.assertEqual(self.chat_room.other_user, self.other_user)


class MessageModelTest(TestCase):
    def setUp(self):
        self.main_user = User.objects.create_user(nickname="하하", social_provider="google", email="haha@haha.com")
        self.other_user = User.objects.create_user(nickname="이이", social_provider="google", email="ee@ee.com")
        self.chat_room = ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)

        self.message = Message.objects.create(room=self.chat_room, sender_nickname=self.main_user.nickname, text="하이")

    def test_message_creation(self):
        self.assertEqual(self.message.sender_nickname, self.main_user.nickname)
        self.assertEqual(self.message.text, "하이")
        self.assertEqual(self.message.room, self.chat_room)
