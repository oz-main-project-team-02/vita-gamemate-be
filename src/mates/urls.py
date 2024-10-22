from django.urls import path

from mates.views import mate_view

urlpatterns = [
    path("register/", mate_view.RegisterMateAPIView.as_view(), name="mate-register"),
    path("", mate_view.MateGameInfoListView.as_view(), name="mate-list"),
    path("<int:game_id>/", mate_view.MateGameInfoListView.as_view(), name="mate-list2"),
]
