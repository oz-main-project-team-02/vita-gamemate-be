from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from games.models import Game
from mates.exceptions import InvalidLevelError
from mates.models import MateGameInfo
from mates.utils import GAME_LEVEL_CHOICES
from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models import User


class RegisterMateAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(nickname="testuser", email="test@example.com", social_provider="google")
        self.game = Game.objects.get(id=1)
        self.url = reverse("mate-register")

        self.token = str(TokenObtainPairSerializer.get_token(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_register_mate_success(self):
        data = {
            "game_id": self.game.id,
            "description": "테스트 코드 너무 좋아",
            "level": "챌린저",
            "request_price": 1000,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_mate_validation_error(self):
        data = {
            "game_id": self.game.id,
            "description": "ㅋㅋ",
            "level": "천재",
            "request_price": 500,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_register_mate_duplicate_game(self):
        MateGameInfo.objects.create(
            user_id=self.user.id,
            game_id=self.game.id,
            description="이미 가입함",
            level="챌린저",
            request_price=1000,
        )

        data = {
            "game_id": self.game.id,
            "description": "같은 게임~",
            "level": "챌린저",
            "request_price": 800,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_mate_invalid_level(self):
        data = {
            "game_id": self.game.id,
            "description": "레벨이 왜케 낮지 못하고 이상하게 적었니",
            "level": "흠흠",
            "request_price": 800,
        }

        with patch("mates.models.MateGameInfo.full_clean", side_effect=InvalidLevelError):
            response = self.client.post(self.url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("잘못된 레벨입니다.", response.data["error"])

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_missing_authorization_header(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = MissingAuthorizationHeader()
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_register_mate_serializer_invalid(self):
        data = {
            "game_id": 30,
            "description": "하하",
            "level": "챌린저",
            "request_price": 800,
        }

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MateGameInfoListViewTest(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            nickname="user1",
            email="user1@example.com",
            gender="male",
            social_provider="google",
        )
        self.user2 = User.objects.create_user(
            nickname="user2",
            email="user2@example.com",
            gender="female",
            social_provider="google",
        )
        self.game = Game.objects.get(id=1)
        self.url = reverse("mate-list")

        # Set up MateGameInfo objects
        MateGameInfo.objects.create(
            user_id=self.user1.id,
            game_id=self.game.id,
            description="User1 Mate Info",
            level="챌린저",
            request_price=500,
        )
        MateGameInfo.objects.create(
            user_id=self.user2.id,
            game_id=self.game.id,
            description="User2 Mate Info",
            level="브론즈",
            request_price=1000,
        )

    def test_mate_game_info_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_game_id_success(self):
        url = reverse("mate-list2", kwargs={"game_id": self.game.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_filter_by_gender(self):
        response = self.client.get(self.url, {"gender": "male"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_filter_by_level(self):
        response = self.client.get(self.url, {"level": "챌린저"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_sort_by_recommendation(self):
        response = self.client.get(self.url, {"sort": "recommendation"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_sort_by_new(self):
        response = self.client.get(self.url, {"sort": "new"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_sort_by_rating_desc(self):
        response = self.client.get(self.url, {"sort": "rating_desc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_sort_by_price_asc(self):
        response = self.client.get(self.url, {"sort": "price_asc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mate_game_info_list_sort_by_price_desc(self):
        response = self.client.get(self.url, {"sort": "price_desc"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
