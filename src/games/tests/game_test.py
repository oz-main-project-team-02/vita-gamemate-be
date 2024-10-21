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

class GameDetailViewTest(APITestCase):
    def setUp(self):
        # Given: 테스트에 사용할 게임 데이터를 미리 생성합
        self.game = Game.objects.create(
            id=1,
            name="Test Game",
            image="test_image.png",
        )

    def test_get_existing_game(self):
        # Given: 데이터베이스에 존재하는 게임 ID
        game_id = self.game.id
        url = reverse("game-detail", args=[game_id])

        # When: 해당 게임 ID로 조회 요청을
        response = self.client.get(url)

        # Then: 응답이 200 OK이고, 반환된 데이터가 정확
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data)  # 'id' 키가 있는지 확인
        self.assertEqual(response.data["name"], self.game.name)

    def test_get_non_existing_game(self):
        # Given: 존재하지 않는 게임 ID
        non_existing_id = 9999
        url = reverse("game-detail", args=[non_existing_id])

        # When: 해당 게임 ID로 조회 요청
        response = self.client.get(url)

        # Then: 응답이 400 Bad Request이고, 오류 메시지가 올바른지 확인
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"error": "해당하는 게임을 찾지 못했습니다."})

class PopularGameListViewTests(APITestCase):
    def setUp(self):
        # Given: 테스트용 게임 데이터를 생성
        Game.objects.create(name="Game A", genre="RPG", rating=4.5, views=100)
        Game.objects.create(name="Game B", genre="Action", rating=4.0, views=150)
        Game.objects.create(name="Game C", genre="Puzzle", rating=3.5, views=50)

    def test_popular_games_list(self):
            # Given: 인기 게임 조회 API URL 설정
            url = reverse('popular-games')

            # When: API에 GET 요청을 보냄
            response = self.client.get(url)

            # Then: 응답 상태 코드가 200 OK이어야 함
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # And: 반환된 데이터의 개수가 2개여야 함
            self.assertEqual(len(response.data), 2)

            # And: 조회수 기준 상위 2개의 게임이 (Game B, Game A) 순서로 반환되어야 함
            self.assertEqual(response.data[0]['name'], "Game B")
            self.assertEqual(response.data[1]['name'], "Game A")