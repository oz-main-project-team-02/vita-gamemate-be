from django.db import models

from games.models import Game
from users.models.user_model import User


class GameRequest(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mate = models.ForeignKey(User, related_name="mate_requests", on_delete=models.CASCADE)
    price = models.IntegerField()
    amount = models.IntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "game_requests"
