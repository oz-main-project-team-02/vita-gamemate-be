from django.db.models.signals import post_save
from django.dispatch import receiver

from users.models import User
from wallets.models import Wallet


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        if not Wallet.objects.filter(user=instance).exists():
            Wallet.objects.create(user=instance)
