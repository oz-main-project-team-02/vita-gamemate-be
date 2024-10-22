from django.db import models


class GameType(models.TextChoices):
    LOL = "lol", "lol"
    OVERWATCH = "overwatch", "overwatch"
    TFT = "tft", "tft"
    BG = "bg", "bg"


class Game(models.Model):
    name = models.CharField(choices=GameType.choices, max_length=255)
    image = models.CharField(max_length=255)
    views = models.IntegerField(default=0)  # 조회수
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
