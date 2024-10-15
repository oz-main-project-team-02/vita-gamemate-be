from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="google@google.com", social_provider="google")
        self.user2 = User.objects.create_user(email="kakao@kakao.com", social_provider="kakao")

    def test_user_created_success(self) -> None:
        self.assertEqual(self.user.email, "google@google.com")
        self.assertEqual(self.user.social_provider, "google")
        self.assertEqual(self.user2.email, "kakao@kakao.com")
        self.assertEqual(self.user2.social_provider, "kakao")

    def test_user_creation_with_duplicate_email(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(email="google@google.com", social_provider="google")

    def test_user_creation_invalid_social_provider(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(email="new@example.com", social_provider="invalid")

    def test_user_creation_invalid_gender(self) -> None:
        with self.assertRaises(ValueError):
            User.objects.create_user(email="gender@gender.com", social_provider="kakao", gender="invalid")
