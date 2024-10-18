from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.ChatRoomCreateView.as_view(), name="chat_room_create"),
    path("rooms/", views.ChatRoomListView.as_view(), name="chat_rooms"),
    path("<int:room_id>/messages/", views.MessageListView.as_view(), name="chat_messages"),
]
