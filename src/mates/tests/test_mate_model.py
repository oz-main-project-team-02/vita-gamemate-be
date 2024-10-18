from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="google@google.com", social_provider="google")

    def test_user_created_success(self) -> None:
        self.assertEqual(self.user.email, "google@google.com")
        self.assertEqual(self.user.social_provider, "google")

    def test_mate_created_successfull(self) -> None: ...
