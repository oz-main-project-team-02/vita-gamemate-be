from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ChatRoom(models.Model):
    main_user = models.ForeignKey(User, related_name="main_user", on_delete=models.CASCADE)
    other_user = models.ForeignKey(User, related_name="other_user", on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("main_user", "other_user")


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="messages")
    sender_nickname = models.CharField(max_length=10, null=False)
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
