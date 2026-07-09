from django.test import TestCase, Client, override_settings
from django.contrib.auth import get_user_model
from menu.models import Category, Dish
from news.models import NewsArticle
from about.models import AboutContent
from contact.models import ContactMessage

User = get_user_model()


@override_settings(STORAGES={
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
})
class PageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.cat = Category.objects.create(name='Test Cat', order=1)
        self.dish = Dish.objects.create(
            category=self.cat, name='Test Dish', price=10.00, is_available=True
        )
        self.news = NewsArticle.objects.create(
            title='Test News', content='Test content', is_published=True
        )
        self.about = AboutContent.objects.create(title='About', content='About text')

    def test_home_page(self):
        r = self.client.get('/pages/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Dish')
        self.assertContains(r, 'Test News')

    def test_menu_page(self):
        r = self.client.get('/pages/menu/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Dish')
        self.assertContains(r, 'Test Cat')

    def test_menu_filter(self):
        r = self.client.get(f'/pages/menu/{self.cat.id}/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test Dish')

    def test_menu_filter_empty(self):
        r = self.client.get('/pages/menu/999/')
        self.assertEqual(r.status_code, 404)

    def test_news_list(self):
        r = self.client.get('/pages/news/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test News')

    def test_news_detail(self):
        r = self.client.get(f'/pages/news/{self.news.id}/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'Test News')
        self.assertContains(r, 'Test content')

    def test_news_detail_404(self):
        r = self.client.get('/pages/news/999/')
        self.assertEqual(r.status_code, 404)

    def test_about_page(self):
        r = self.client.get('/pages/about/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'About')

    def test_contact_page(self):
        r = self.client.get('/pages/contact/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'csrfmiddlewaretoken')

    def test_contact_post(self):
        r = self.client.post('/pages/contact/', {
            'name': 'Test', 'email': 'test@test.com', 'message': 'Hello'
        })
        self.assertEqual(r.status_code, 302)  # redirect after success
        self.assertTrue(ContactMessage.objects.filter(name='Test').exists())

    def test_login_page(self):
        r = self.client.get('/login/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'csrfmiddlewaretoken')

    def test_register_page(self):
        r = self.client.get('/register/')
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, 'csrfmiddlewaretoken')

    def test_register_post(self):
        r = self.client.post('/register/', {
            'username': 'newuser',
            'email': 'new@test.com',
            'password': 'testpass123',
            'password2': 'testpass123',
        })
        self.assertEqual(r.status_code, 302)  # redirect after success
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        r = self.client.post('/register/', {
            'username': 'failuser',
            'email': 'fail@test.com',
            'password': 'testpass123',
            'password2': 'different',
        })
        self.assertEqual(r.status_code, 200)  # re-render with errors
        self.assertFalse(User.objects.filter(username='failuser').exists())

    def test_menu_unavailable_hidden(self):
        Dish.objects.create(
            category=self.cat, name='Hidden', price=5.00, is_available=False
        )
        r = self.client.get('/pages/menu/')
        self.assertNotContains(r, 'Hidden')

    def test_news_unpublished_hidden(self):
        NewsArticle.objects.create(
            title='Draft', content='draft', is_published=False
        )
        r = self.client.get('/pages/news/')
        self.assertNotContains(r, 'Draft')

    def test_base_template_brand(self):
        r = self.client.get('/pages/')
        self.assertContains(r, 'LONDON')
        self.assertContains(r, 'GRILL HOUSE')
