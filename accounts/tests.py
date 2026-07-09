from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import CustomUser

class AccountsTests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.refresh_url = reverse('auth-refresh')
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone': '123456789'
        }

    def test_register_success(self):
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

    def test_register_no_password(self):
        data = self.user_data.copy()
        data.pop('password')
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_duplicate_username(self):
        self.client.post(self.register_url, self.user_data)
        response = self.client.post(self.register_url, self.user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_success(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_wrong_password(self):
        CustomUser.objects.create_user(**self.user_data)
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_refresh_success(self):
        CustomUser.objects.create_user(**self.user_data)
        login_response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpassword123'
        })
        refresh_token = login_response.data['refresh']
        response = self.client.post(self.refresh_url, {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_invalid(self):
        response = self.client.post(self.refresh_url, {'refresh': 'invalidtoken'})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
