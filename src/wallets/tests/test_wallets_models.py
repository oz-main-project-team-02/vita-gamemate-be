from django.test import TestCase

from users.models import User
from wallets.models.wallets_model import Wallet


class WalletModelTest(TestCase):

    def setUp(self):
        # Given
        self.user = User.objects.create_user(email="testuser@example.com", password="password123", social_provider="google")

    def test_wallet_creation(self):
        # When
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # Then
        self.assertEqual(wallet.user, self.user)
        self.assertEqual(wallet.coin, 100)
        self.assertIsNotNone(wallet.created_at)
        self.assertIsNotNone(wallet.updated_at)

    def test_wallet_default_coin_value(self):
        # When
        wallet = Wallet.objects.create(user=self.user)

        # Then
        self.assertEqual(wallet.coin, 0)

    def test_wallet_update_coin(self):
        # Given
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # When
        wallet.coin = 200
        wallet.save()

        # Then
        wallet.refresh_from_db()
        self.assertEqual(wallet.coin, 200)

    def test_wallet_deletion(self):
        # Given
        wallet = Wallet.objects.create(user=self.user, coin=100)

        # When
        wallet.delete()

        # Then
        self.assertFalse(Wallet.objects.filter(user=self.user).exists())
