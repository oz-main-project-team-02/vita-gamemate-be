from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletBalanceViewTest(APITestCase):

    def setUp(self):
        # Given
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")
        self.wallet = Wallet.objects.create(user=self.user, coin=100)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_wallet_balance(self):
        # When:조회하는 요청을 보냈을 때
        url = reverse("user-coin-wallet")
        response = self.client.get(url)

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["coin_balance"], 100)

    def test_wallet_not_found(self):
        # Given
        new_user = User.objects.create_user(email="newuser@example.com", password="password123", social_provider="google")

        refresh = RefreshToken.for_user(new_user)
        new_user_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {new_user_token}")

        # When: 사용자가 잔액을 조회하려고 할 때
        url = reverse("user-coin-wallet")
        response = self.client.get(url)

        # Then:
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")


class WalletRechargeViewTest(APITestCase):

    def setUp(self):
        # Given
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")
        self.wallet = Wallet.objects.create(user=self.user, coin=100)

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_wallet_recharge_success(self):
        # Given:
        url = reverse("user-coin-recharge")

        # When: 사용자가 50 코인을 충전하려고 요청을 보냈을 때
        response = self.client.post(url + "?coin=50", format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.coin, 150)

    def test_wallet_recharge_invalid_coin_amount(self):
        # Given
        url = reverse("user-coin-recharge")

        # When: 잘못된 coin 값(0)을 보내는 요청
        response = self.client.post(url + "?coin=0", format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["coin"][0]), "충전할 코인 양은 1 이상이어야 합니다.")

    def test_wallet_recharge_invalid_coin_type(self):
        # Given
        url = reverse("user-coin-recharge")

        # When: 잘못된 형식의 coin 값(문자열)을 보내는 요청
        response = self.client.post(url + "?coin=invalid", format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["coin"][0]), "유효한 정수(integer)를 넣어주세요.")


class NoWalletViewTest(APITestCase):

    def setUp(self):
        # Given
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.access_token}")

    def test_wallet_recharge_no_wallet(self):
        # Given
        url = reverse("user-coin-recharge")

        # When: 사용자가 100 코인을 충전하려고 요청을 보냈을 때
        response = self.client.post(url + "?coin=100", format="json")

        # Then
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")
