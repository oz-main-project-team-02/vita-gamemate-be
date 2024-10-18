# rest_framework의 serializers 모듈을 임포트합니다.
from rest_framework import serializers

# 현재 디렉토리의 models 모듈에서 ChatRoom, Message 모델을 임포트합니다.
from .models import ChatRoom, Message


# Message 모델에 대한 시리얼라이저 클래스입니다.
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message  # Message 모델을 기반으로 합니다.
        fields = "__all__"  # 모든 필드를 포함시킵니다.


# ChatRoom 모델에 대한 시리얼라이저 클래스입니다.
class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()  # 최신 메시지 필드를 동적으로 가져옵니다.
    main_user_nickname = serializers.SerializerMethodField()  # 메인 사용자의 닉네임을 가져오는 필드입니다.
    other_user_nickname = serializers.SerializerMethodField()  # 상대방 사용자의 닉네임을 가져오는 필드입니다.
    # messages = MessageSerializer(many=True, read_only=True, source="messages.all")  # 해당 채팅방의 메시지 목록을 가져옵니다.

    class Meta:
        model = ChatRoom  # ChatRoom 모델을 기반으로 합니다.
        # 시리얼라이즈할 필드들을 지정합니다.
        fields = ("id", "main_user_nickname", "other_user_nickname", "latest_message")

    # 최신 메시지를 가져오는 메소드입니다.
    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(room=obj).order_by("-timestamp").first()  # 최신 메시지를 조회합니다.
        if latest_msg:
            return latest_msg.text  # 최신 메시지의 내용을 반환합니다.
        return None  # 메시지가 없다면 None을 반환합니다.

    # main_user의 닉네임을 반환하는 메소드입니다.
    def get_main_user_nickname(self, obj):
        return obj.main_user.main_user_nickname

    # other_user의 이메일을 반환하는 메소드입니다.
    def get_other_user_nickname(self, obj):
        return obj.other_user.other_user_nickname
