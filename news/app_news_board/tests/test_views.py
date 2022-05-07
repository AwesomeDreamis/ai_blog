from django.test import TestCase
from django.urls import reverse
from app_news_board.models import News
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.test import Client


class NewsListPageTest(TestCase):
    def test_news_list_page(self):
        url = reverse('news_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_news_list_exists_at_desired_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'news/news_list.html')


class CreatePageTest(TestCase):
    def test_create_page(self):
        url = reverse('create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_create_exists_at_desired_location(self):
        response = self.client.get('/create/')
        self.assertTemplateUsed(response, 'news/create.html')

    def test_create_post(self):
        response = self.client.post('/create/', {'content': 'content', 'is_active': False})
        self.assertEqual(response.status_code, 200)


class NewsDetailPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test",)
        user.set_password('12345')
        user.save()

        cls.news = News.objects.create(
            author=user,
            content="test",
            is_active=False
        )

    def test_news_list_exists_at_desired_location(self):
        response = self.client.get(f'/{self.news.id}/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'news/news_detail.html')

    def test_comment_post(self):
        response = self.client.post(f'/{self.news.id}/', {'user': self.news.author, 'text': 'text'})
        self.assertEqual(response.status_code, 200)


class NewsEditPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test",)
        user.set_password('12345')
        user.save()

        cls.news = News.objects.create(
            author=user,
            content="test",
            is_active=False
        )

    def test_news_edit_exists_at_desired_location(self):
        logged_in = self.client.login(username='test', password='12345')
        response = self.client.get(f'/{self.news.id}/edit/')

        self.assertTrue(logged_in)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/edit.html')


class NewsDeletePageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="test",)
        user.set_password('12345')
        user.save()

        cls.news = News.objects.create(
            author=user,
            content="test",
            is_active=False
        )

    def test_news_delete_exists_at_desired_location(self):
        logged_in = self.client.login(username='test', password='12345')
        response = self.client.get(f'/{self.news.id}/delete/')

        self.assertTrue(logged_in)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'news/delete.html')
