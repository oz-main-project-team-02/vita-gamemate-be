from django.test import TestCase

from users.exceptions import UserNotFound
from users.models import User


class TestUserManager(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(id=1, nickname="test", email="asf@asdf.com", social_provider="google")

    def test_get_user_by_id(self) -> None:
        self.assertEqual(User.objects.get_user_by_id(user_id=1), self.user)

    def test_get_user_by_id_error(self) -> None:
        with self.assertRaises(UserNotFound):
            User.objects.get_user_by_id(999)

    def test_get_user_by_email_and_social_provider(self) -> None:
        self.assertEqual(
            User.objects.get_user_by_email_and_social_provider(email="asf@asdf.com", social_provider="google"),
            self.user,
        )

    def test_get_user_by_email_and_social_provider_error(self) -> None:
        with self.assertRaises(UserNotFound):
            User.objects.get_user_by_email_and_social_provider(email="111", social_provider="google")

    def test_get_user_by_nickname(self) -> None:
        self.assertEqual(
            User.objects.get_user_by_nickname(user_nickname="test"),
            self.user,
        )

    def test_get_user_by_nickname_error(self) -> None:
        with self.assertRaises(UserNotFound):
            User.objects.get_user_by_nickname(user_nickname="error")
