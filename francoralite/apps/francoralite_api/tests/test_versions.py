import pytest

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

@pytest.mark.django_db
class TestVersions(APITestCase):
    """
    This class tests versions
    """

    def test_get_versions(self):
         url = reverse('versions')
         response = self.client.get(url)

         self.assertEqual(response.status_code, status.HTTP_200_OK)
         self.assertEqual(len(response.data), 4)
         self.assertEqual(response.data["python"][0:6], "3.11.9")
         self.assertEqual(response.data["django"], (4,2,13,"final",0))
