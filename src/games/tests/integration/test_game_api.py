from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from games.models.game_model import Game, GameType
from games.serializers.game_serializers import GameSerializer


class GameListViewTest(APITestCase):
    def setUp(self):
        self.game1 = Game.objects.get(
            name=GameType.LOL,
        )
        self.game2 = Game.objects.get(
            name=GameType.OVERWATCH,
        )
        self.url = reverse("game-list")

    def test_game_list_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        games = Game.objects.all()
        serializer = GameSerializer(games, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_game_list_failure(self):
        Game.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


class GameDetailViewTest(APITestCase):
    def setUp(self):
        self.game = Game.objects.get(
            name=GameType.LOL,
        )
        self.valid_url = reverse("game-detail", kwargs={"game_id": self.game.id})
        self.invalid_url = reverse("game-detail", kwargs={"game_id": 9999})

    def test_game_detail_success(self):
        response = self.client.get(self.valid_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = GameSerializer(self.game)
        self.assertEqual(response.data, serializer.data)

    def test_game_detail_not_found(self):
        response = self.client.get(self.invalid_url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class PopularGameListViewTest(APITestCase):
    def setUp(self):
        self.game1 = Game.objects.get(
            name=GameType.LOL,
        )
        self.game2 = Game.objects.get(
            name=GameType.TFT,
        )
        self.game3 = Game.objects.get(
            name=GameType.BG,
        )
        self.url = reverse("popular-games")

    def test_popular_game_list_success(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        popular_games = Game.objects.order_by("-views")[:2]
        serializer = GameSerializer(popular_games, many=True)

        self.assertEqual(response.data, serializer.data)

    def test_popular_game_list_not_found(self):
        Game.objects.all().delete()

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "인기 게임 조회에 실패하였습니다.")
