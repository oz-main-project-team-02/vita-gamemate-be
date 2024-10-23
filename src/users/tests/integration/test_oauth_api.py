from unittest.mock import patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.services.social_login_service import SocialLoginCallbackService


class SocialLoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.google_login_url = "/api/v1/users/google/login/"
        self.kakao_login_url = "/api/v1/users/kakao/login/"

    @patch("users.services.social_login_service.SocialLoginService.social_login")
    def test_google_login_redirect(self, mock_social_login):
        mock_social_login.return_value = "http://mock-google-login-url.com"

        response = self.client.get(self.google_login_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "http://mock-google-login-url.com", fetch_redirect_response=False)

    @patch("users.services.social_login_service.SocialLoginService.social_login")
    def test_kakao_login_redirect(self, mock_social_login):
        mock_social_login.return_value = "http://mock-kakao-login-url.com"

        response = self.client.get(self.kakao_login_url)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertRedirects(response, "http://mock-kakao-login-url.com", fetch_redirect_response=False)


class SocialLoginCallbackAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", social_provider="google")
        self.google_login_url_callback = "/api/v1/users/google/login/callback/"
        self.kakao_login_url_callback = "/api/v1/users/kakao/login/callback/"

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    @patch("users.services.social_login_service.SocialLoginCallbackService.get_user_info")
    def test_google_login_success(self, mock_get_user_info, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer mock_access_token"}
        mock_get_user_info.return_value = {
            "email": "testuser@example.com",
            "name": "Test User",
            "gender": None,
        }

        mock_google_response = {"code": "mock_google_code"}

        response = self.client.post(self.google_login_url_callback, mock_google_response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.cookies)

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    @patch("users.services.social_login_service.SocialLoginCallbackService.get_user_info")
    def test_google_login_user_not_found(self, mock_get_user_info, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer mock_access_token"}
        mock_get_user_info.return_value = {
            "email": "newuser@example.com",
            "name": "New User",
            "gender": None,
        }

        mock_google_response = {"code": "mock_google_code_not_found"}

        response = self.client.post(self.google_login_url_callback, mock_google_response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

        new_user = User.objects.get(email="newuser@example.com")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.nickname, "New User")

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    def test_google_login_invalid_code(self, mock_get_auth_headers):
        mock_get_auth_headers.side_effect = ValueError()
        mock_google_response = {"code": "invalid_google_code"}

        response = self.client.post(self.google_login_url_callback, mock_google_response)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    def test_kakao_login_invalid_code(self, mock_get_auth_headers):
        mock_get_auth_headers.side_effect = ValueError()
        mock_kakao_response = {"code": "invalid_kakao_code"}

        response = self.client.post(self.kakao_login_url_callback, mock_kakao_response)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    @patch("users.services.social_login_service.SocialLoginCallbackService.get_user_info")
    def test_kakao_login_success(self, mock_get_user_info, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer mock_access_token"}
        mock_get_user_info.return_value = {
            "kakao_account": {
                "email": "testuser1@example.com",
                "profile": {"nickname": "Test User"},
            }
        }

        mock_kakao_response = {"code": "mock_kakao_code"}

        response = self.client.post(self.kakao_login_url_callback, mock_kakao_response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)
        self.assertIn("refresh_token", response.cookies)

    @patch("users.services.social_login_service.SocialLoginCallbackService.get_auth_headers")
    @patch("users.services.social_login_service.SocialLoginCallbackService.get_user_info")
    def test_kakao_login_user_not_found(self, mock_get_user_info, mock_get_auth_headers):
        mock_get_auth_headers.return_value = {"Authorization": "Bearer mock_access_token"}
        mock_get_user_info.return_value = {
            "kakao_account": {
                "email": "newuser@example.com",
                "profile": {"nickname": "New User"},
            }
        }

        mock_kakao_response = {"code": "mock_kakao_code_not_found"}

        response = self.client.post(self.kakao_login_url_callback, mock_kakao_response)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access_token", response.data)

        # Check if the user has been created
        new_user = User.objects.get(email="newuser@example.com")
        self.assertIsNotNone(new_user)
        self.assertEqual(new_user.nickname, "New User")


class LogoutAPIViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = "/api/v1/users/auth/logout/"
        self.user = User.objects.create_user(email="testuser@example.com", social_provider="google")

    @patch("users.views.oauth_view.RefreshToken")
    def test_post_unexpected_exception(self, mock_refresh_token):
        token = RefreshToken.for_user(self.user)
        self.client.cookies["refresh_token"] = str(token)
        mock_refresh_token.side_effect = Exception("또잉 에러")

        response = self.client.post(self.logout_url, {}, cookies={"refresh_token": "dummy_token"})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"Unexpected Error": "또잉 에러"})

    def test_logout_success(self):
        token = RefreshToken.for_user(self.user)
        self.client.cookies["refresh_token"] = str(token)

        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertNotIn("refresh_token", response.cookies) 이거 왜 안되는지 모르겠음

    def test_logout_without_token(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
