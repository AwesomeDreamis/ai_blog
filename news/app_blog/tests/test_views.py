from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app_users.models import Profile
from app_news_board.models import News


class BlogPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username="testuser",)
        user.set_password('12345')
        user.save()

        cls.profile = Profile.objects.create(
            user=user,
            city="moscow",
            phone="555",
            is_verified=False,
            news_count=0
        )

    def test_blog_page(self):
        response = self.client.get(f'/blog/{self.profile.user.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog.html')

    def test_csv_exists_at_desired_location(self):
        response = self.client.get(f'/blog/upload/')
        self.assertEqual(response.status_code, 200)

    def test_csv_upload(self):
        logged_in = self.client.login(username='testuser', password='12345')
        # success_upload = False

        news_count = News.objects.count()

        with open('app_blog/tests/data.csv', 'r', encoding='utf-8-sig') as f:
            response = self.client.post('/blog/upload/', {'name': 'file', 'file': f})

        news_count1 = News.objects.count()

        # if news_count == 3:
        #     success_upload = True

        self.assertTrue(logged_in)
        # self.assertTrue(success_upload)
        self.assertNotEqual(news_count, news_count1)
        self.assertRedirects(response, '/')
