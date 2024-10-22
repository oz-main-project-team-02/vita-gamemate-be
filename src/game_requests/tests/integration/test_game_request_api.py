from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from game_requests.models import GameRequest
from games.models import Game
from mates.models import MateGameInfo
from users.exceptions import MissingAuthorizationHeader
from users.models import User


class GameRequestAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            nickname="사용자임",
            email="user1@example.com",
            gender="male",
            social_provider="google",
        )
        self.mate = User.objects.create_user(
            nickname="mate임",
            email="user2@example.com",
            gender="female",
            social_provider="google",
        )
        self.game = Game.objects.get(
            name="lol",
        )
        MateGameInfo.objects.create(
            user_id=self.mate.id,
            game=self.game,
            description="gg",
            level="챌린저",
            request_price=1000,
        )

        self.url_create = reverse("game-request-create", kwargs={"user_id": self.mate.id})
        self.url_ordered = reverse("ordered-game-request")
        self.url_received = reverse("received-game-request")

        self.token = str(TokenObtainPairSerializer.get_token(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_create_game_request_success(self):
        response = self.client.post(
            self.url_create,
            {
                "game_id": self.game.id,
                "price": 1000,
                "amount": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_game_request_user_not_found(self):
        response = self.client.post(
            reverse("game-request-create", kwargs={"user_id": 456}),
            {
                "game_id": self.game.id,
                "price": 500,
                "amount": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_game_request_to_self(self):
        MateGameInfo.objects.create(
            user_id=self.user.id,
            game=self.game,
            description="gg",
            level="챌린저",
            request_price=1000,
        )
        response = self.client.post(
            reverse("game-request-create", kwargs={"user_id": self.user.id}),
            {
                "game_id": self.game.id,
                "price": 500,
                "amount": 1,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_game_request_invalid_data(self):
        response = self.client.post(
            self.url_create,
            {
                "game_id": self.game.id,
                "price": -500,
                "amount": 1,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("price", response.data)

    def test_ordered_game_requests_success(self):
        GameRequest.objects.create(
            user_id=self.user.id,
            mate_id=self.mate.id,
            game_id=self.game.id,
            price=500,
            amount=1,
        )

        response = self.client.get(self.url_ordered)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["mate_nickname"], self.mate.nickname)

    def test_received_game_requests_success(self):
        self.token = str(TokenObtainPairSerializer.get_token(self.mate).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

        GameRequest.objects.create(
            user_id=self.user.id,
            mate_id=self.mate.id,
            game_id=self.game.id,
            price=500,
            amount=1,
        )

        response = self.client.get(self.url_received)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["user_nickname"], self.user.nickname)

    def test_ordered_game_requests_no_requests(self):
        response = self.client.get(self.url_ordered)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_received_game_requests_no_requests(self):
        response = self.client.get(self.url_received)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_missing_authorization_header(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = MissingAuthorizationHeader()
        response = self.client.post(self.url_create, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.url_received, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response = self.client.get(self.url_ordered, {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
