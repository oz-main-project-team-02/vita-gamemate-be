from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletBalanceViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # 유저 생성 (지갑은 자동으로 생성됨)
        cls.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

        # 유저의 토큰 생성
        refresh = RefreshToken.for_user(cls.user)
        cls.access_token = str(refresh.access_token)

        # 지갑의 초기 잔액을 설정
        cls.wallet = Wallet.objects.get(user=cls.user)
        cls.wallet.coin = 100
        cls.wallet.save()

    def setUp(self):
        # 각 테스트마다 인증 헤더 설정
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_wallet_balance_success(self):
        # When: 지갑 잔액을 조회하는 요청을 보낸다.
        url = reverse("user-coin-wallet")
        response = self.client.get(url)

        # Then: 잔액이 정상적으로 반환되는지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["coin"], 100)

    def test_wallet_recharge(self):
        # Given: 지갑에 50 코인을 충전
        url = reverse("user-coin-recharge")
        data = {"coin": 50}
        response = self.client.post(url, data, format="json")

        # Then: 충전이 성공적으로 완료되는지 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 잔액이 150으로 증가했는지 확인
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.coin, 150)
