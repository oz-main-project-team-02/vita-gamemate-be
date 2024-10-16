from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from games.models.game_model import Game


class GameListViewTest(APITestCase):
    def setUp(self):
        # Given: 테스트를 위한 초기 데이터 설정
        Game.objects.create(name="LOL", image="image1.png")
        Game.objects.create(name="OVERWATCH", image="image2.png")

    def test_get_game_list(self):
        # When: 게임 목록 조회 API 호출
        url = reverse("game-list")
        response = self.client.get(url, format="json")

        # Then: 응답 결과 검증
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["name"], "LOL")
        self.assertEqual(response.data[0]["image"], "image1.png")
