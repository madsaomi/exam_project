from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from menu.models import Category, Dish

User = get_user_model()


class CategoryModelTest(APITestCase):
    def setUp(self):
        self.cat1 = Category.objects.create(name='Salatlar', description='Yengil taomlar', order=2)
        self.cat2 = Category.objects.create(name='Ichimliklar', description='Sovuq ichimliklar', order=1)

    def test_str(self):
        self.assertEqual(str(self.cat1), 'Salatlar')

    def test_ordering(self):
        categories = list(Category.objects.all())
        self.assertEqual(categories[0], self.cat2)
        self.assertEqual(categories[1], self.cat1)


class CategoryAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.user = User.objects.create_user(username='user', password='userpass123')
        self.category = Category.objects.create(name='Shirinliklar', description='Desertlar', order=1)
        self.list_url = reverse('category-list')
        self.detail_url = reverse('category-detail', args=[self.category.id])

    def test_list_categories(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_category_anon(self):
        response = self.client.post(self.list_url, {'name': 'Yangi', 'description': 'Test', 'order': 1})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.list_url, {'name': 'Yangi', 'description': 'Test', 'order': 1})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_category_user(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.list_url, {'name': 'Yangi', 'description': 'Test', 'order': 1})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_category(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.detail_url, {'name': 'Yangilangan'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_category_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class DishAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin2', password='adminpass123')
        self.category = Category.objects.create(name='Asosiy taomlar', description='Issiq taomlar', order=1)
        self.dish1 = Dish.objects.create(
            category=self.category, name='Osh', description='Milliy taom',
            price=25000, is_available=True, order=1
        )
        self.dish2 = Dish.objects.create(
            category=self.category, name='Lag\'mon', description='Uyg\'ur taomi',
            price=20000, is_available=True, order=2
        )
        self.list_url = reverse('dish-list')

    def test_list_dishes(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_dish_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {
            'category': self.category.id, 'name': 'Manti', 'description': 'Bug\'da pishirilgan',
            'price': 22000, 'is_available': True, 'order': 3
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_filter_by_category(self):
        response = self.client.get(self.list_url, {'category': self.category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']) if 'results' in response.data else len(response.data), 2)

    def test_search_by_name(self):
        response = self.client.get(self.list_url, {'search': 'Osh'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)