from django.db import models


class Gametype(models.TextChoices):
    LOL = "lol", "리그 오브 레전드"
    OVERWATCH = "overwatch", "오버워치"
    TFT = "tft", "전략적 팀 전투"
    BG = "bg", "배틀그라운드"


class Game(models.Model):
    name = models.CharField(choices=Gametype.choices, max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
