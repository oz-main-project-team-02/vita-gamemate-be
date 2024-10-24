# from unittest.mock import patch
#
# from django.test import TestCase
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APIClient
#
#
# class UserStatusAPITestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse("user-status")
#
#     @patch("django_redis.get_redis_connection")
#     def test_user_is_online_true(self, mock_redis):
#         # Redis에서 "True" 반환을 모의
#         mock_redis.return_value.get.return_value = b"True"
#
#         response = self.client.get(self.url, {"user_id": 1})
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), {"is_online": True})
#
#     @patch("django_redis.get_redis_connection")
#     def test_user_is_online_false(self, mock_redis):
#         # Redis에서 "False" 반환을 모의
#         mock_redis.return_value.get.return_value = b"False"
#
#         response = self.client.get(self.url, {"user_id": 1})
#
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.json(), {"is_online": False})
#
#     @patch("django_redis.get_redis_connection")
#     def test_user_is_online_missing(self, mock_redis):
#         # Redis에서 값을 찾지 못했을 때 None을 반환
#         mock_redis.return_value.get.return_value = None
#
#         response = self.client.get(self.url, {"user_id": 1})
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json(), {"error": "사용자에게 is_online값이 없습니다."})
#
#     def test_user_id_missing(self):
#         response = self.client.get(self.url)
#
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.json(), {"error": "쿼리 파라미터로 user_id 를 보내주세요."})
