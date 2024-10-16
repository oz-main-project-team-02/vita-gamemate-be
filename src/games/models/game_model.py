from django.db import models

class Game(models.Model):
    GameChoices = [
        ('LOL', '리그 오브 레전드'),
        ('OVERWATCH', '오버워치')
    ]
    name = models.CharField(choices=GameChoices, default='',max_length=255)
    image = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name