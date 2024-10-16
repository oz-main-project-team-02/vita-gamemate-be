from django.test import TestCase

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletModelTest(TestCase):

    def setUp(self):
        # Given: 사용자 생성
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

    def test_wallet_creation(self):
        # When: 지갑 생성
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # Then: 지갑이 정상적으로 생성되었는지 확인
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.coin, 100)
        self.assertIsNotNone(wallet.created_at)
        self.assertIsNotNone(wallet.updated_at)

    def test_wallet_default_coin_value(self):
        # When: 지갑 생성 시 coin 값을 제공하지 않음
        wallet = Wallet.objects.create(user=self.user)

        # Then: coin의 기본 값이 0인지 확인
        self.assertEqual(wallet.coin, 0)

    def test_wallet_update_coin(self):
        # Given: 초기 coin 값이 100인 지갑을 생성
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # When: 지갑의 coin 값을 200으로 업데이트
        wallet.coin = 200
        wallet.save()

        # Then: coin 값이 200으로 업데이트되었는지 확인
        wallet.refresh_from_db()  # DB에서 최신 데이터를 다시 불러옴
        self.assertEqual(wallet.coin, 200)

    def test_wallet_deletion(self):
        # Given: 지갑 생성
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # When: 지갑 삭제
        wallet.delete()

        # Then: 지갑이 더 이상 존재하지 않는지 확인
        self.assertFalse(Wallet.objects.filter(user=self.user).exists())
