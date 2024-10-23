from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class MateSearchAPITest(APITestCase):
    def setUp(self):
        self.mate1 = User.objects.create(nickname="mate_one", is_mate=True, email="test@example.com")
        self.mate2 = User.objects.create(nickname="mate_two", is_mate=True, email="test2@example.com")
        self.mate3 = User.objects.create(nickname="mate_three", is_mate=True, email="test3@example.com")
        self.non_mate = User.objects.create(nickname="non_mate", is_mate=False, email="test4@example.com")
        self.url = "/api/v1/mates/search/"

    def test_search_mates_by_nickname(self):
        response = self.client.get(self.url, {"search": "mate"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_search_mates_no_results(self):
        response = self.client.get(self.url, {"search": "unknown"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_search_query(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)
