from django.db import models

from games.models import Game
from mates.managers import MateGameInfoManager
from users.models.user_model import User


class MateGameInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_column="game_id")
    description = models.TextField()
    image = models.ImageField(upload_to="mates/images/", blank=True, null=True)
    level = models.CharField(max_length=255, blank=True, null=True)
    request_price = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = MateGameInfoManager()

    class Meta:
        db_table = "mate_game_info"
        unique_together = (("user", "game"),)
