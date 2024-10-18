from django.urls import path

from mates.views import mate_view

urlpatterns = [
    path("register/", mate_view.RegisterMateAPIView.as_view(), name="mate-register"),
]
