from django.db import models

from game_requests.models import GameRequest


class Review(models.Model):
    game_request = models.ForeignKey(GameRequest, on_delete=models.CASCADE, db_column="game_request_id")
    rating = models.FloatField(max_length=5)
    content = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "review"
