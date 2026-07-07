from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from about.models import AboutContent

User = get_user_model()


class AboutContentAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin", password="adminpass123"
        )
        self.url = reverse("about-detail")

    def test_get_about_anon(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_about_returns_content(self):
        response = self.client.get(self.url)
        self.assertIn("title", response.data)
        self.assertIn("content", response.data)

    def test_update_about_anon(self):
        response = self.client.put(self.url, {"content": "New content"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_about_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.put(self.url, {"content": "Admin content"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["content"], "Admin content")

    def test_singleton_auto_create(self):
        AboutContent.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(AboutContent.objects.count(), 1)
