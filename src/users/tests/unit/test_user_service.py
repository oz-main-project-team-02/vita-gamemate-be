import unittest
from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.exceptions import APIException
from rest_framework_simplejwt.tokens import AccessToken

from users.exceptions import (
    InvalidAuthorizationHeader,
    MissingAuthorizationHeader,
    TokenMissing,
    UserNotFound,
)
from users.models.user_model import User
from users.services.social_login_service import (
    SocialLoginCallbackService,
    SocialLoginService,
)
from users.services.user_service import UserService


class UserServiceTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", nickname="testuser", social_provider="google")
        self.valid_token = str(AccessToken.for_user(self.user))

    def test_missing_authorization_header(self):
        with self.assertRaises(MissingAuthorizationHeader):
            UserService.get_user_from_token(None)

    def test_invalid_authorization_header(self):
        with self.assertRaises(InvalidAuthorizationHeader):
            UserService.get_user_from_token("InvalidHeader")

    def test_token_missing(self):
        with self.assertRaises(TokenMissing):
            UserService.get_user_from_token("Bearer ")

    @patch("users.models.user_model.User.objects.get_user_by_id")
    @patch("rest_framework_simplejwt.tokens.AccessToken")
    def test_user_not_found(self, mock_access_token, mock_get_user_by_id):
        mock_access_token.return_value.get.return_value = 999
        mock_get_user_by_id.side_effect = UserNotFound

        with self.assertRaises(UserNotFound):
            UserService.get_user_from_token(f"Bearer {self.valid_token}")

    @patch("users.models.user_model.User.objects.get_user_by_id")
    @patch("rest_framework_simplejwt.tokens.AccessToken")
    def test_successful_user_return(self, mock_access_token, mock_get_user_by_id):
        mock_access_token.return_value.get.return_value = self.user.id
        mock_get_user_by_id.return_value = self.user

        user = UserService.get_user_from_token(f"Bearer {self.valid_token}")

        self.assertEqual(user, self.user)

    # @patch("rest_framework_simplejwt.tokens.AccessToken")
    # def test_api_exception(self, mock_access_token):
    #     mock_access_token.side_effect = Exception("Unexpected error")
    #
    #     with self.assertRaises(APIException):
    #         UserService.get_user_from_token(f"Bearer {self.valid_token}")


class TestSocialLoginService(unittest.TestCase):

    def setUp(self):
        self.service = SocialLoginService()
        self.service.client_id = "test_client_id"
        self.service.redirect_uri = "http://localhost:8000/callback"
        self.service.login_uri = "http://login.example.com"

    def test_social_login_with_scope(self):
        context = {"scope": "profile email"}
        expected_url = f"{self.service.login_uri}?client_id={self.service.client_id}&redirect_uri={self.service.redirect_uri}&response_type=code&scope=profile email"

        result = self.service.social_login(context)

        self.assertEqual(result, expected_url)

    def test_social_login_without_scope(self):
        expected_url = (
            f"{self.service.login_uri}?client_id={self.service.client_id}&redirect_uri={self.service.redirect_uri}&response_type=code"
        )

        result = self.service.social_login()

        self.assertEqual(result, expected_url)


class TestSocialLoginCallbackService(unittest.TestCase):

    def setUp(self):
        self.service = SocialLoginCallbackService()
        self.service.client_id = "test_client_id"
        self.service.client_secret = "test_client_secret"
        self.service.redirect_uri = "http://localhost:8000/callback"
        self.service.token_uri = "http://token.example.com"
        self.service.profile_uri = "http://profile.example.com"

    def test_create_token_request_data(self):
        code = "test_code"
        expected_data = {
            "grant_type": self.service.grant_type,
            "client_id": self.service.client_id,
            "client_secret": self.service.client_secret,
            "redirect_uri": self.service.redirect_uri,
            "code": code,
        }

        result = self.service.create_token_request_data(code)

        self.assertEqual(result, expected_data)

    @patch("requests.post")
    def test_get_auth_headers(self, mock_post):
        token_response = Mock()
        token_response.status_code = 200
        token_response.json.return_value = {"access_token": "test_access_token"}
        mock_post.return_value = token_response

        token_request_data = {
            "grant_type": "authorization_code",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "http://localhost:8000/callback",
            "code": "test_code",
        }

        expected_headers = {"Authorization": "Bearer test_access_token"}

        result = self.service.get_auth_headers(token_request_data)

        self.assertEqual(result, expected_headers)
        mock_post.assert_called_once_with(
            self.service.token_uri,
            data=token_request_data,
            headers={"Content-type": self.service.content_type},
        )

    @patch("requests.post")
    def test_get_auth_headers_error(self, mock_post):
        token_response = Mock()
        token_response.status_code = 400
        token_response.text = "Bad Request"
        mock_post.return_value = token_response

        token_request_data = {
            "grant_type": "authorization_code",
            "client_id": "test_client_id",
            "client_secret": "test_client_secret",
            "redirect_uri": "http://localhost:8000/callback",
            "code": "test_code",
        }

        with self.assertRaises(ValueError):
            self.service.get_auth_headers(token_request_data)

    @patch("requests.get")
    def test_get_user_info(self, mock_get):
        user_info_response = Mock()
        user_info_response.json.return_value = {"id": "12345", "email": "test@example.com"}
        mock_get.return_value = user_info_response

        auth_headers = {"Authorization": "Bearer test_access_token"}
        expected_user_info = {"id": "12345", "email": "test@example.com"}

        result = self.service.get_user_info(auth_headers)

        self.assertEqual(result, expected_user_info)
        mock_get.assert_called_once_with(self.service.profile_uri, headers=auth_headers)


if __name__ == "__main__":
    unittest.main()
