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
            raise ValidationError(e)
        user.save(using=self._db)
        return user

    def get_user_by_id(self, user_id: int):
        try:
            return self.get(id=user_id)
        except self.model.DoesNotExist:
            return None

    def get_user_by_email_and_social_provider(self, email: str, social_provider: str):
        try:
            return self.get(email=email, social_provider=social_provider)
        except self.model.DoesNotExist:
            return None

    def get_user_by_nickname(self, user_nickname: str):
        try:
            return self.get(nickname=user_nickname)
        except self.model.DoesNotExist:
            return None
