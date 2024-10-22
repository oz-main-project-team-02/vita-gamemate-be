from django.core.exceptions import ValidationError
from django.test import TestCase

from users.models import User


class UserModelTestCase(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email="google@google.com", social_provider="google")
        self.user2 = User.objects.create_user(email="kakao@kakao.com", social_provider="kakao")
        self.user3 = User.objects.create_user(email="nickname@nickname.com", social_provider="kakao", nickname="test")

    def test_user_created_success(self) -> None:
        self.assertEqual(self.user.nickname, None)
        self.assertEqual(self.user.email, "google@google.com")
        self.assertEqual(self.user2.email, "kakao@kakao.com")
        self.assertEqual(self.user.social_provider, "google")
        self.assertNotEqual(self.user.password, None)
        self.assertEqual(self.user.gender, None)
        self.assertEqual(self.user.profile_image, None)
        self.assertEqual(self.user.birthday, None)
        self.assertEqual(self.user.description, None)
        self.assertEqual(self.user.social_provider, "google")
        self.assertEqual(self.user2.social_provider, "kakao")
        self.assertEqual(self.user.is_online, True)
        self.assertEqual(self.user.is_mate, False)
        self.assertEqual(self.user.is_active, True)
        self.assertEqual(self.user.is_staff, False)
        self.assertEqual(self.user.is_superuser, False)
        self.assertEqual(self.user.last_login, None)
        self.assertNotEqual(self.user.updated_at, None)
        self.assertNotEqual(self.user.created_at, None)

    def test_user_creation_with_duplicate_email(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="google@google.com", social_provider="google")

    def test_user_creation_invalid_social_provider(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="new@example.com", social_provider="invalid")

    def test_user_creation_invalid_gender(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="gender@gender.com", social_provider="kakao", gender="invalid")

    def test_user_creation_invalid_state(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="gende1@gender.com", social_provider="kakao", is_active=False)

    def test_user_creation_invalid_state2(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="gender2@gender.com", social_provider="kakao", is_online=False)

    def test_user_creation_invalid_state3(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="gender4@gender.com", social_provider="kakao", is_mate=True)

    def test_user_creation_invalid_permission2(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="googe@google.com", social_provider="google", is_staff=True)

    def test_user_creation_invalid_permission3(self) -> None:
        with self.assertRaises(ValidationError):
            User.objects.create_user(email="ggle@google.com", social_provider="google", is_superuser=True)

    def test_user_return(self) -> None:
        self.assertEqual(str(self.user3), "test")
