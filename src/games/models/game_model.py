from django.db import models


class Gametype(models.TextChoices):
    LOL = "리그오브레전드", "리그오브레전드"
    OVERWATCH = "오버워치", "오버워치"
    TFT = "전략적팀전투", "전략적팀전투"
    BG = "배틀그라운드", "배틀그라운드"


class Game(models.Model):
    name = models.CharField(choices=Gametype.choices, max_length=255)
    image = models.CharField(max_length=255)
    views = models.IntegerField(default=0)  # 조회수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
