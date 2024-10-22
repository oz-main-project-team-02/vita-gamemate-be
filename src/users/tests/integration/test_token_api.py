from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User


class CustomTokenRefreshAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", social_provider="google")
        self.refresh_token = str(RefreshToken.for_user(self.user))

    def test_refresh_token_success(self):
        self.client.cookies["refresh_token"] = self.refresh_token

        response = self.client.get("/api/v1/users/auth/accesstoken/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

    def test_refresh_token_not_in_cookies(self):
        response = self.client.get("/api/v1/users/auth/accesstoken/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_token_invalid(self):
        self.client.cookies["refresh_token"] = "invalid_token"

        response = self.client.get("/api/v1/users/auth/accesstoken/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data)
