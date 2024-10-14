# type: ignore
from typing import Any

from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError


class UserManager(BaseUserManager):
    def create_user(self, email: str, social_provider: str, **extra_fields: Any):
        email = self.normalize_email(email)
        social_provider = social_provider.lower()

        user = self.model(email=email, social_provider=social_provider, **extra_fields)
        user.set_unusable_password()
        try:
            user.full_clean()
        except ValidationError as e:
            raise ValueError(str(e))
        user.save(using=self._db)
        return user
