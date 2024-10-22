from django.utils import timezone

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from users.managers import UserManager
from users.models.user_model import User

from .models import ChatRoom, Message


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        try:
            self.room_id = self.scope["url_route"]["kwargs"]["room_id"]  # URL 경로에서 방 ID를 추출

            if not await self.check_room_exists(self.room_id):  # 방이 존재하는지 확인
                raise ValueError("채팅방이 존재하지 않습니다.")

            group_name = self.get_group_name(self.room_id)  # 방 ID를 사용하여 그룹 이름 가져옴

            await self.channel_layer.group_add(group_name, self.channel_name)  # 현재 채널을 그룹에 추가
            await self.accept()  # WebSocket 연결 수락

        except ValueError as e:  # 값 오류가 있을 경우 (예: 방이 존재하지 않음), 오류 메시지를 보내고 연결을 종료
            await self.send_json({"error": str(e)})
            await self.close()

    async def disconnect(self, close_code):
        try:
            group_name = self.get_group_name(self.room_id)  # 방 ID를 사용하여 그룹 이름 가져옴
            await self.channel_layer.group_discard(group_name, self.channel_name)  # 현재 채널을 그룹에서 제거

        except Exception as e:
            pass

    async def receive_json(self, content):
        try:
            # 수신된 JSON에서 필요한 정보를 추출
            message = content["message"]
            sender_nickname = content["sender_nickname"]
            main_user_nickname = content.get("main_user_nickname")
            other_user_nickname = content.get("other_user_nickname")

            # 두 닉네임이 모두 제공되었는지 확인
            if not main_user_nickname or not other_user_nickname:
                raise ValueError("채팅 사용자 모두의 닉네임이 필요합니다.")

            # 제공된 닉네임을 사용하여 방을 가져오거나 생성
            room = await self.get_or_create_room(main_user_nickname, other_user_nickname)

            # room_id 속성을 업데이트
            self.room_id = str(room.id)

            # 그룹 이름을 가져오기
            group_name = self.get_group_name(self.room_id)

            # 수신된 메시지를 데이터베이스에 저장
            await self.save_message(room, sender_nickname, message)

            # 메시지를 전체 그룹에 전송
            await self.channel_layer.group_send(
                group_name, {"type": "chat_message", "message": message, "sender_nickname": sender_nickname}  # 발신자 닉네임 정보 추가
            )

        except ValueError as e:
            # 값 오류가 있을 경우, 오류 메시지를 전송
            await self.send_json({"error": str(e)})

    async def chat_message(self, event):
        try:
            # 이벤트에서 메시지와 발신자 닉네임을 추출
            message = event["message"]
            sender_nickname = event["sender_nickname"]  # 발신자 닉네임 정보 추출

            # 추출된 메시지와 발신자 닉네임을 JSON으로 전송
            await self.send_json({"message": message, "sender_nickname": sender_nickname})
        except Exception as e:
            await self.send_json({"error": "메시지 전송 실패"})

    @staticmethod
    def get_group_name(room_id):
        # 방 ID를 사용하여 고유한 그룹 이름을 구성
        return f"chat_room_{room_id}"

    @database_sync_to_async
    def get_or_create_room(self, main_user_nickname, other_user_nickname):
        main_user, _ = User.objects.get_or_create(nickname=main_user_nickname)
        other_user, _ = User.objects.get_or_create(nickname=other_user_nickname)

        room, created = ChatRoom.objects.get_or_create(main_user=main_user, other_user=other_user)
        return room

    @database_sync_to_async
    def save_message(self, room, sender_nickname, message_text):
        # 발신자 닉네임과 메시지 텍스트가 제공되었는지 확인
        if not sender_nickname or not message_text:
            raise ValueError("발신자 닉네임 및 메시지 텍스트가 필요합니다.")

        # 메시지를 생성하고 데이터베이스에 저장
        Message.objects.create(room=room, sender_nickname=sender_nickname, text=message_text)

        # 새로운 메시지가 생성된 후 ChatRoom의 updated_at을 갱신
        room.updated_at = timezone.now()
        room.save()

    @database_sync_to_async
    def check_room_exists(self, room_id):
        # 주어진 ID로 채팅방이 존재하는지 확인
        return ChatRoom.objects.filter(id=room_id).exists()


