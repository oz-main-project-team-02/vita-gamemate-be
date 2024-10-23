from django.test import TestCase

from wallets.serializers.wallets_serializers import WalletRechargeSerializer


class WalletValidateTest(TestCase):

    def test_zero_coin(self):
        data = {"coin": 0}
        serializer = WalletRechargeSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("coin", serializer.errors)
