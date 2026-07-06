from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from contact.models import ContactMessage

User = get_user_model()


class ContactMessageModelTest(APITestCase):
    def setUp(self):
        self.message = ContactMessage.objects.create(
            name='Ali', email='ali@example.com', message='Salom, savolim bor'
        )

    def test_str(self):
        self.assertEqual(str(self.message), 'Ali')


class ContactMessageAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.user = User.objects.create_user(username='user', password='userpass123')
        self.message = ContactMessage.objects.create(
            name='Vali', email='vali@example.com', message='Test xabar', is_read=False
        )
        self.list_url = reverse('contact-list')

    def test_send_message_anon(self):
        data = {'name': 'Anvar', 'email': 'anvar@example.com', 'message': 'Yordam kerak'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_send_message_without_email(self):
        data = {'name': 'Anvar', 'message': 'Yordam kerak'}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_messages_anon(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_messages_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_list_messages_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_filter_by_is_read(self):
        self.client.force_authenticate(user=self.admin)
        ContactMessage.objects.create(
            name='O\'qilgan', email='oqilgan@example.com', message='Javob berilgan', is_read=True
        )
        response = self.client.get(self.list_url, {'is_read': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)