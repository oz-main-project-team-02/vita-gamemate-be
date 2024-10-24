from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from game_requests.models import GameRequest
from games.models import Game
from reviews.models import Review
from users.models.user_model import User


class ReviewListViewTest(TestCase):
    # 리뷰 리스트 조회

    def setUp(self):
        # Given: 리뷰 데이터가 데이터베이스에 존재할 때

        self.user1 = User.objects.create(nickname="user1", email="user1@example.com")
        self.user2 = User.objects.create(nickname="user2", email="user2@example.com")
        self.game = Game.objects.create(name="리그오브레전드")
        # GameRequest 생성 시 user_id와 mate_id 제공
        self.game_request = GameRequest.objects.create(
            user_id=self.user1.id, mate_id=self.user2.id, game=self.game, price=3000  # user_id에 user1 할당  # mate_id에 user2 할당
        )
        self.game_request.title = "게임 목록 조회"

        Review.objects.create(game_request=self.game_request, rating=5.0, content="와 진짜 재밌다", created_at="2024-10-17T15:35:42Z")
        Review.objects.create(game_request=self.game_request, rating=1.0, content="와 진짜 노잼", created_at="2024-10-17T15:35:42Z")

    def test_review_list_view(self):
        # When: 리뷰 목록을 요청했을 때
        url = reverse("reviews")

        response = self.client.get(url)

        # Then: 최신 순으로 리뷰가 반환되고, 한 페이지에 최대 10개의 리뷰가 있어야 한다
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # 데이터베이스에 2개의 리뷰가 있으므로
        self.assertEqual(response.data["results"][0]["content"], "와 진짜 노잼")  # 최신 리뷰가 첫 번째로 와야 함
        self.assertEqual(response.data["results"][1]["content"], "와 진짜 재밌다")


class GameReviewCreateAPIViewTest(APITestCase):

    def setUp(self):
        # Given: 필요한 데이터 준비
        self.user1 = User.objects.create(nickname="user1", email="user1@example.com")
        self.user2 = User.objects.create(nickname="user2", email="user2@example.com")
        self.game = Game.objects.create(name="리그오브레전드")

        # GameRequest 생성
        self.game_request = GameRequest.objects.create(
            user_id=self.user1.id,
            mate_id=self.user2.id,
            game=self.game,
            price=3000,
            # user_id에 user1 할당  # mate_id에 user2 할당
        )
        self.game_request.title = "게임 목록 조회"

        Review.objects.create(game_request=self.game_request, rating=5.0, content="와 진짜 재밌다", created_at="2024-10-17T15:35:42Z")
        Review.objects.create(game_request=self.game_request, rating=1.0, content="와 진짜 노잼", created_at="2024-10-17T15:35:42Z")

        self.refresh = RefreshToken.for_user(self.user1)

        # URL 정의
        self.url = reverse("review-write", args=[self.game_request.id])

    def test_create_review_success(self):  # 성공
        # When: 올바른 데이터로 리뷰를 생성 요청

        data = {"game_request": self.game_request.id, "rating": 5.0, "content": "아 짱 좋아요"}
        response = self.client.post(self.url, data, format="json", headers={"Authorization": f"Bearer {str(self.refresh.access_token)}"})

        # Then: 성공적으로 리뷰가 생성되고 201 응답을 받아야 함
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 3)  # 리뷰가 하나 생성되어야 함
        self.assertEqual(response.data["content"], "아 짱 좋아요")  # 내용 확인

    def test_create_review_missing_authorization(self):  # 성공
        # When: 인증 없이 리뷰 생성 요청

        data = {"game_request": self.game_request.id, "rating": 5.0, "content": "아 짱 좋아요"}
        response = self.client.post(self.url, data, format="json")
        # Then: 401 Unauthorized 응답을 받아야 함
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data["detail"], "자격 인증데이터(authentication credentials)가 제공되지 않았습니다.")

    def test_create_review_game_request_not_found(self):  # 성공
        # When: 존재하지 않는 게임 요청으로 리뷰 생성 요청
        self.client.force_authenticate(user=self.user1)
        data = {"game_request": 99999, "rating": 5.0, "content": "아 짱 좋아요"}  # 존재하지 않는 ID
        response = self.client.post(self.url, data, format="json")

        # Then: 404 Not Found 응답을 받아야 함
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["game_request"][0]), f'유효하지 않은 pk "{data["game_request"]}" - 객체가 존재하지 않습니다.')

    def test_create_review_invalid_rating(self):
        # When: 잘못된 평점으로 리뷰 생성 요청
        self.client.force_authenticate(user=self.user1)

        data = {"game_request": self.game_request.id, "rating": 6.0, "content": "아 짱 좋아요"}  # 유효하지 않은 평점
        response = self.client.post(self.url, data, format="json")

        # Then: 400 Bad Request 응답을 받아야 하고 오류 메시지가 포함되어야 함
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["rating"][0]), "평점은 1.0에서 5.0 사이여야 합니다.")
