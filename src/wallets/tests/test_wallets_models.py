from django.test import TestCase

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletModelTest(TestCase):

    def setUp(self):
        # Given: 유저 생성 (지갑은 post_save 시그널로 자동 생성됨)
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

    def test_wallet_creation(self):
        # When: 유저에 대한 지갑이 자동으로 생성되었는지 확인
        wallet = Wallet.objects.get(user=self.user)  # 지갑 자동 생성 확인

        # Then: 지갑이 올바르게 생성되었는지 확인
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.coin, 0)  # 기본 코인 값이 0인지 확인
        self.assertIsNotNone(wallet.created_at)
        self.assertIsNotNone(wallet.updated_at)

    def test_wallet_update_coin(self):
        # Given: 자동 생성된 지갑을 가져옴
        wallet = Wallet.objects.get(user=self.user)

        # When: 지갑 코인 값 업데이트
        wallet.coin = 200
        wallet.save()

        # Then: 값이 제대로 반영되었는지 확인
        wallet.refresh_from_db()
        self.assertEqual(wallet.coin, 200)

    def test_wallet_deletion(self):
        # Given: 자동 생성된 지갑을 가져옴
        wallet = Wallet.objects.get(user=self.user)

        # When: 지갑 삭제
        wallet.delete()

        # Then: 해당 유저에 대한 지갑이 삭제되었는지 확인
        self.assertFalse(Wallet.objects.filter(user=self.user).exists())


class WalletCreationTest(TestCase):

    def test_wallet_creation_on_user_creation(self):
        # 유저 생성
        user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

        # When: 유저에 대한 지갑이 자동으로 생성되었는지 확인
        self.assertTrue(Wallet.objects.filter(user=user).exists())

        # Then: 지갑이 하나만 생성되었는지 확인 (중복 방지)
        self.assertEqual(Wallet.objects.filter(user=user).count(), 1)
