from django.db import models

from game_requests.managers import GameRequestManager
from games.models import Game
from users.models.user_model import User


class GameRequest(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, db_column="game_id")
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user_id")
    mate = models.ForeignKey(User, on_delete=models.CASCADE, db_column="mate_id", related_name="mate")
    price = models.PositiveIntegerField()
    amount = models.PositiveIntegerField(default=1)
    status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = GameRequestManager()

    class Meta:
        db_table = "game_requests"
