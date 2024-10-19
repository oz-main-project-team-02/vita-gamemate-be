from django.db import models


class Gametype(models.TextChoices):
    LOL = "리그 오브 레전드", "리그 오브 레전드"
    OVERWATCH = "오버워치", "오버워치"
    TFT = "전략적 팀 전투", "전략적 팀 전투"
    BG = "배틀그라운드", "배틀그라운드"


class Game(models.Model):
    name = models.CharField(choices=Gametype.choices, max_length=255)
    image = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
