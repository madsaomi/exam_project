from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from news.models import NewsArticle

User = get_user_model()


class NewsArticleModelTest(APITestCase):
    def setUp(self):
        self.article1 = NewsArticle.objects.create(
            title='Birinchi yangilik', content='Matn 1', is_published=True
        )
        self.article2 = NewsArticle.objects.create(
            title='Ikkinchi yangilik', content='Matn 2', is_published=True
        )

    def test_str(self):
        self.assertEqual(str(self.article1), 'Birinchi yangilik')

    def test_ordering(self):
        articles = list(NewsArticle.objects.all())
        self.assertEqual(articles[0], self.article2)
        self.assertEqual(articles[1], self.article1)


class NewsArticleAPITest(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(username='admin', password='adminpass123')
        self.article = NewsArticle.objects.create(
            title='Test yangilik', content='Test matni', is_published=True
        )
        self.list_url = reverse('newsarticle-list')
        self.detail_url = reverse('newsarticle-detail', args=[self.article.id])

    def test_list_news(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_news_anon(self):
        response = self.client.post(self.list_url, {'title': 'Yangi', 'content': 'Matn', 'is_published': True})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_news_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.post(self.list_url, {'title': 'Yangi', 'content': 'Matn', 'is_published': True})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_detail_news(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_news_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.patch(self.detail_url, {'title': 'Yangilangan sarlavha'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_news_admin(self):
        self.client.force_authenticate(user=self.admin)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_filter_published(self):
        NewsArticle.objects.create(title='Draft', content='Nashr etilmagan', is_published=False)
        response = self.client.get(self.list_url, {'is_published': True})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_search_title(self):
        response = self.client.get(self.list_url, {'search': 'Test'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)