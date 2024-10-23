from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from game_requests.models import GameRequest
from games.models import Game
from reviews.models import Review
from users.models import User


class ReviewAPITestCase(TestCase):

    def setUp(self):
        # 테스트에 필요한 유저, 게임, 게임 의뢰, 리뷰 생성
        self.user = User.objects.create_user(email="user1@example.com", password="password123", nickname="User1", social_provider="google")
        self.mate = User.objects.create_user(email="mate1@example.com", password="password123", nickname="Mate1", social_provider="google")
        self.game = Game.objects.create(name="리그 오브 레전드", image="image1.jpg")

        # GameRequest 생성 (user와 mate 객체를 직접 전달)
        self.game_request = GameRequest.objects.create(user_id=self.user.id, mate_id=self.mate.id, game=self.game, price=500, amount=1)

        # 리뷰 생성
        for i in range(30):
            Review.objects.create(game_request=self.game_request, rating=5, content=f"리뷰 내용 {i}")

    # def test_user_review_list(self):
    #     # 특정 사용자의 전체 리뷰 목록 조회 테스트
    #
    #     url = reverse("review-list", kwargs={"user_id": self.user.id})
    #
    #     response = self.client.get(url, query_params={"page": 1})
    #
    #     # 디버그: 응답 데이터를 출력하여 확인
    #     print(f"응답 데이터: {response.data}")
    #
    #     # 200 응답 상태 코드 확인
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #
    #     # 응답 데이터 확인
    #     self.assertEqual(response.data["count"], 30)
    #     self.assertEqual(len(response.data["results"]), 10)
    #     self.assertIn("next", response.data)
    #     self.assertIn("previous", response.data)
    #     self.assertIsNotNone(response.data["next"])

    def test_game_request_review_list(self):
        # 특정 게임 의뢰의 리뷰 목록 조회 테스트
        url = reverse("reviews-request", kwargs={"game_request_id": self.game_request.id})
        response = self.client.get(url, query_params={"page": 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터 확인 (총 15개 중 페이지 당 10개만 반환)
        self.assertEqual(response.data["count"], 30)
        self.assertEqual(len(response.data["results"]), 10)  # 페이지 당 10개
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIsNotNone(response.data["next"])  # 다음 페이지 링크가 있어야 함

    def test_user_game_review_list(self):
        # 특정 사용자의 특정 게임에 대한 리뷰 목록 조회 테스트
        url = reverse("review-game", kwargs={"user_id": self.user.id, "game_id": self.game.id})
        response = self.client.get(url, query_params={"page": 1})

        # 200 응답 상태 코드 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 응답 데이터 확인 (15개 중 페이지 당 10개만 반환)
        self.assertEqual(response.data["count"], 30)
        self.assertEqual(len(response.data["results"]), 10)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIsNotNone(response.data["next"])  # 다음 페이지 링크가 있어야 함
