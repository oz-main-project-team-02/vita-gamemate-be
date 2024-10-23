from rest_framework import serializers

from .models import ChatRoom, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"


class ChatRoomSerializer(serializers.ModelSerializer):
    latest_message = serializers.SerializerMethodField()
    main_user_nickname = serializers.SerializerMethodField()
    other_user_nickname = serializers.SerializerMethodField()
    other_user_id = serializers.SerializerMethodField()
    other_user_profile_image = serializers.SerializerMethodField()
    # messages = MessageSerializer(many=True, read_only=True, source="messages.all")
    latest_message_time = serializers.SerializerMethodField()
    updated_at = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = (
            "id",
            "main_user_nickname",
            "other_user_nickname",
            "other_user_id",
            "other_user_profile_image",
            "latest_message",
            "latest_message_time",
            "updated_at",
        )

    # 최신 메시지를 가져오는 메소드
    def get_latest_message(self, obj):
        latest_msg = Message.objects.filter(room=obj).order_by("-updated_at").first()
        if latest_msg:
            # latest_message와 last_message_time을 함께 반환
            self.context["latest_message_time"] = latest_msg.updated_at
            return latest_msg.text
        return None

    # 최신 메시지의 시간을 가져오는 메소드
    def get_latest_message_time(self, obj):
        return self.context.get("latest_message_time")

    # main_user의 닉네임을 반환하는 메소드
    def get_main_user_nickname(self, obj):
        print("Object type11:", type(obj))
        print("get_main_user_nickname called with obj:", obj)
        return obj.main_user.nickname

    # other_user의 닉네임을 반환하는 메소드
    def get_other_user_nickname(self, obj):
        return obj.other_user.nickname

    def get_other_user_id(self, obj):
        return obj.other_user.id

    def get_other_user_profile_image(self, obj):
        return obj.other_user.profile_image.url if obj.other_user.profile_image else None

    def get_updated_at(self, obj):
        return obj.updated_at
