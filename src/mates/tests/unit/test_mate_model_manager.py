from django.core.exceptions import ValidationError
from django.test import TestCase

from games.models import Game
from mates.exceptions import InvalidLevelError
from mates.models import MateGameInfo
from mates.utils import GAME_LEVEL_CHOICES
from users.models import User


class MateGameInfoModelAndManagerTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(nickname="testuser", email="test@example.com", social_provider="google")
        self.game = Game.objects.get(id=1)

    def test_create_mate_game_info_success(self):
        mategameinfo = MateGameInfo.objects.create(
            user_id=self.user.id, game=self.game, description="gg", level="챌린저", request_price=1000
        )

        self.assertEqual(mategameinfo.user, self.user)
        self.assertEqual(mategameinfo.game, self.game)
        self.assertEqual(mategameinfo.level, "챌린저")
        self.assertEqual(mategameinfo.request_price, 1000)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_mate)

    def test_create_mate_game_info_invalid_data(self):
        with self.assertRaises(InvalidLevelError):
            MateGameInfo.objects.create(
                user_id=self.user.id,
                game=self.game,
                description="나는 천재",
                level="바보",
                request_price=800,
            )

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_mate)

    def test_create_mate_game_info_missing_required_fields(self):
        with self.assertRaises(ValidationError):
            MateGameInfo.objects.create(user_id=self.user.id, game=self.game, description="Missing price", level="챌린저")

        self.user.refresh_from_db()
        self.assertFalse(self.user.is_mate)

    def test_user_already_mate(self):
        self.user.is_mate = True
        self.user.save()

        MateGameInfo.objects.create(user_id=self.user.id, game=self.game, description="Already a mate", level="챌린저", request_price=500)

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_mate)
