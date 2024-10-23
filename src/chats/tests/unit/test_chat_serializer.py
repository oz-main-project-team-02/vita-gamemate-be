from django.test import TestCase

from chats.models import ChatRoom, Message
from chats.serializers import ChatRoomSerializer
from users.models import User


class ChatRoomSerializerTest(TestCase):
    def setUp(self):
        self.main_user = User.objects.create_user(
            nickname="서강준",
            social_provider="google",
            email="haha@haha.com",
            profile_image="서강준.jpg",
        )

        self.other_user = User.objects.create_user(
            nickname="아이유",
            social_provider="google",
            email="ee@ee.com",
            profile_image="아이유.png",
        )
        self.chat_room = ChatRoom.objects.create(main_user=self.main_user, other_user=self.other_user)

    def test_chat_room_serializer(self):
        serializer = ChatRoomSerializer(self.chat_room)
        data = serializer.data

        self.assertEqual(data["main_user_nickname"], self.main_user.nickname)
        self.assertEqual(data["other_user_nickname"], self.other_user.nickname)

    def test_get_latest_message_with_no_messages(self):
        serializer = ChatRoomSerializer(self.chat_room)

        self.assertIsNone(serializer.get_latest_message(self.chat_room))
        self.assertIsNone(serializer.get_latest_message_time(self.chat_room))

    def test_get_latest_message_with_messages(self):
        message = Message.objects.create(room=self.chat_room, sender_nickname=self.main_user.nickname, text="하이!")
        serializer = ChatRoomSerializer(self.chat_room)

        self.assertEqual(serializer.get_latest_message(self.chat_room), message.text)
        self.assertIsNotNone(serializer.get_latest_message_time(self.chat_room))
        self.assertEqual(serializer.get_latest_message_time(self.chat_room), message.updated_at)

    def test_get_main_user_nickname(self):
        serializer = ChatRoomSerializer(self.chat_room)

        self.assertEqual(serializer.get_main_user_nickname(self.chat_room), self.main_user.nickname)

    def test_get_other_user_nickname(self):
        serializer = ChatRoomSerializer(self.chat_room)

        self.assertEqual(serializer.get_other_user_nickname(self.chat_room), self.other_user.nickname)

    # def test_get_other_user_profile_image(self):
    #     serializer = ChatRoomSerializer(self.chat_room)

    #     self.assertEqual(serializer.get_other_user_profile_image(self.chat_room), self.other_user.profile_image.url)
