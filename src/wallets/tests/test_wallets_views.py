from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletBalanceViewTest(APITestCase):

    def setUp(self):
        # Given: 사용자가 있고, 지갑에 코인이 존재하는 경우
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")
        self.wallet = Wallet.objects.create(user=self.user, coin=100)
        self.client.force_authenticate(user=self.user)

    def test_wallet_balance(self):
        # When: 사용자가 자신의 지갑 잔액을 조회하는 요청을 보냈을 때
        url = reverse("user-coin-wallet", kwargs={"user_id": self.user.id})
        response = self.client.get(url)

        # Then: 200 OK 응답과 함께 잔액 정보를 반환해야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user_id"], self.user.id)
        self.assertEqual(response.data["coin_balance"], 100)

    def test_wallet_not_found(self):
        # Given: 지갑이 없는 사용자
        new_user = User.objects.create_user(email="newuser@example.com", password="password123", social_provider="google")
        self.client.force_authenticate(user=new_user)

        # When: 사용자가 잔액을 조회하려고 할 때
        url = reverse("user-coin-wallet", kwargs={"user_id": new_user.id})
        response = self.client.get(url)

        # Then: 404 Not Found 응답을 반환해야 함
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")


class WalletRechargeViewTest(APITestCase):

    def setUp(self):
        # Given: 사용자가 있고, 지갑에 초기 코인이 100인 상태
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")
        self.wallet = Wallet.objects.create(user=self.user, coin=100)
        self.client.force_authenticate(user=self.user)

    def test_wallet_recharge_success(self):
        # Given: 지갑이 있고, 사용자가 인증된 상태
        url = reverse("user-coin-recharge", kwargs={"user_id": self.user.id})

        # When: 사용자가 50 코인을 충전하려고 요청을 보냈을 때
        response = self.client.post(url + "?coin=50", format="json")

        # Then: 200 OK 응답과 함께 코인이 충전되어야 함
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.wallet.refresh_from_db()
        self.assertEqual(self.wallet.coin, 150)

    def test_wallet_recharge_invalid_coin_amount(self):
        # Given: 지갑이 있는 상태에서 0 코인을 충전하려고 요청
        url = reverse("user-coin-recharge", kwargs={"user_id": self.user.id})

        # When: 잘못된 coin 값(0)을 보내는 요청
        response = self.client.post(url + "?coin=0", format="json")
        # Then: 400 Bad Request 응답과 함께 '충전할 코인 양은 1 이상이어야 합니다.' 메시지를 반환
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["coin"][0]), "충전할 코인 양은 1 이상이어야 합니다.")

    def test_wallet_recharge_invalid_coin_type(self):
        # Given: 지갑이 있는 상태에서 잘못된 코인 형식(문자열)으로 요청
        url = reverse("user-coin-recharge", kwargs={"user_id": self.user.id})

        # When: 잘못된 형식의 coin 값(문자열)을 보내는 요청
        response = self.client.post(url + "?coin=invalid", format="json")

        # Then: 400 Bad Request 응답과 함께 '충전할 코인 양을 유효한 숫자로 입력해야 합니다.' 메시지를 반환
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data["coin"][0]), "유효한 정수(integer)를 넣어주세요.")


class NoWalletViewTest(APITestCase):

    def setUp(self):
        # Given: 사용자가 있고, 초기에는 지갑이 없는 상태
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")
        self.client.force_authenticate(user=self.user)

    def test_wallet_recharge_no_wallet(self):
        # Given: 지갑이 없는 상태
        url = reverse("user-coin-recharge", kwargs={"user_id": self.user.id})

        # When: 사용자가 100 코인을 충전하려고 요청을 보냈을 때
        response = self.client.post(url + "?coin=100", format="json")

        # Then: 404 Not Found 응답과 함께 지갑이 없다는 메시지를 반환해야 함
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "지갑을 찾을 수 없습니다.")
