from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.files.storage import default_storage
from django.db import models

from users.managers import UserManager


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
    profile_image = models.ImageField(upload_to="profiles/", storage=default_storage, blank=True, null=True)
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

    objects = UserManager()

    def clean(self) -> None:
        super().clean()
        if self.is_superuser:
            raise ValidationError({"error": "어드민으로 생성할 수 없습니다."})

        if self.is_staff:
            raise ValidationError({"error": "관리자로 생성할 수 없습니다."})

        if not self.is_active:
            raise ValidationError({"error": "사용자의 상태를 변경할 수 없습니다."})

        if self.is_mate:
            raise ValidationError({"error": "사용자를 mate로 변경할 수 없습니다."})

        if not self.is_online:
            raise ValidationError({"error": "사용자의 현재 상태를 변경할 수 없습니다."})

        if self.social_provider and self.social_provider not in dict(SocialProvider.choices):
            raise ValidationError({"error": "올바른 소셩 제공자를 입력해주세요."})

        if self.gender and self.gender not in dict(Gender.choices):
            raise ValidationError({"error": "올바른 성별을 입력해주세요."})

    def __str__(self) -> str:
        return self.nickname
