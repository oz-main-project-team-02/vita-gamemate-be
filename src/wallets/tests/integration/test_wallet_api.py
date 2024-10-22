from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models import User
from wallets.models.wallets_model import Wallet


class WalletViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(nickname="testuser", email="asdf@adsf.com", social_provider="google")
        self.wallet = Wallet.objects.get(user=self.user)

        self.token = str(TokenObtainPairSerializer.get_token(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.token)

    def test_get_wallet_balance_success(self):
        url = reverse("user-coin-wallet")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["coin"], self.wallet.coin)

    def test_get_wallet_balance_not_found(self):
        Wallet.objects.filter(user=self.user).delete()
        url = reverse("user-coin-wallet")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")

    def test_recharge_wallet_success(self):
        url = reverse("user-coin-recharge")
        data = {"coin": 50}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.coin, 50)

    def test_recharge_wallet_invalid_coin(self):
        url = reverse("user-coin-recharge")
        data = {"coin": 0}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("coin", response.data)

    def test_recharge_wallet_user_not_found(self):
        Wallet.objects.filter(user=self.user).delete()
        url = reverse("user-coin-recharge")
        data = {"coin": 50}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")

    def test_recharge_wallet_missing_auth(self):
        self.client.credentials()
        url = reverse("user-coin-recharge")
        data = {"coin": 50}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_missing_authorization_header(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = MissingAuthorizationHeader()
        response = self.client.get(reverse("user-coin-wallet"), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response2 = self.client.post(reverse("user-coin-recharge"), {})
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_invalid_authorization_header(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = InvalidAuthorizationHeader()
        response = self.client.get(reverse("user-coin-wallet"), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        response2 = self.client.post(reverse("user-coin-recharge"), {})
        self.assertEqual(response2.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_token_missing(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = TokenMissing()
        response = self.client.get(reverse("user-coin-wallet"), {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response2 = self.client.post(reverse("user-coin-recharge"), {})
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("users.services.user_service.UserService.get_user_from_token")
    def test_user_not_found(self, mock_get_user_from_token):
        mock_get_user_from_token.side_effect = UserNotFound()
        response = self.client.get(reverse("user-coin-wallet"), {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response2 = self.client.post(reverse("user-coin-recharge"), {})
        self.assertEqual(response2.status_code, status.HTTP_404_NOT_FOUND)
