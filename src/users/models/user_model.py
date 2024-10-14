import uuid

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models

from users.managers import UserManager  # type: ignore


class SocialProvider(models.TextChoices):
    GOOGLE = "google", "Google"
    KAKAO = "kakao", "Kakao"


class Gender(models.TextChoices):
    MALE = "male", "Male"
    FEMALE = "female", "Female"


class User(AbstractBaseUser, PermissionsMixin):
    nickname = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True, null=True)
    profile_image = models.CharField(max_length=255, blank=True, null=True)
    birthday = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    social_provider = models.CharField(
        max_length=10,
        choices=SocialProvider.choices,
        default=None,
        null=True,
        blank=True,
    )
    is_online = models.BooleanField(default=True)
    is_mate = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()  # type: ignore

    def clean(self) -> None:
        super().clean()
        if self.social_provider and self.social_provider not in dict(SocialProvider.choices):
            raise ValidationError({"social_provider": "Invalid social provider"})

        if self.gender and self.gender not in dict(Gender.choices):
            raise ValidationError({"gender": "Invalid gender"})

    def __str__(self) -> str:
        return self.email
