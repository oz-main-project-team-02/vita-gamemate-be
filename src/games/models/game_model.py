from django.db import models


class Gametype(models.TextChoices):
    LOL = "리그오브레전드", "리그오브레전드"
    OVERWATCH = "오버워치", "오버워치"
    # 게임 종류 추후 추가


class Game(models.Model):
    name = models.CharField(choices=Gametype.choices, max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
