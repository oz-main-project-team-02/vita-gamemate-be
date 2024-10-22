from django.test import TestCase

from games.models import Game
from games.models.game_model import GameType


class GameModelTest(TestCase):
    def setUp(self):
        self.game = Game.objects.get(name="lol")

    def test_game_creation(self):
        self.assertEqual(self.game.name, GameType.LOL)

    def test_game_str_method(self):
        # __str__ 메서드가 올바르게 작동하는지 확인
        self.assertEqual(str(self.game), GameType.LOL.label)
