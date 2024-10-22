from django.test import TestCase

from game_requests.models import GameRequest
from games.models import Game
from users.models.user_model import User


class GameRequestModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            nickname="user1",
            email="user1@example.com",
            gender="male",
            social_provider="google",
        )
        self.mate = User.objects.create_user(
            nickname="user2",
            email="user2@example.com",
            gender="female",
            social_provider="google",
        )
        self.game = Game.objects.get(
            name="lol",
        )

    def test_create_game_request(self):
        game_request = GameRequest.objects.create(
            game=self.game,
            user_id=self.user.id,
            mate_id=self.mate.id,
            price=1000,
            amount=2,
        )

        self.assertEqual(game_request.game, self.game)
        self.assertEqual(game_request.user, self.user)
        self.assertEqual(game_request.mate, self.mate)
        self.assertEqual(game_request.price, 1000)
        self.assertEqual(game_request.amount, 2)
        self.assertTrue(game_request.status)
