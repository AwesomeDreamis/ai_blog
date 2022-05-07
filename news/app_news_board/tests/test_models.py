from django.test import TestCase
from django.urls import reverse
from app_news_board.models import News, Images, Comment
from datetime import datetime


class NewsModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.news = News.objects.create(
            content="test",
            is_active=False
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.news.content, str)
        self.assertIsInstance(self.news.created_at, datetime)
        self.assertIsInstance(self.news.updated_at, datetime)
        self.assertIsInstance(self.news.is_active, bool)


class CommentModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.comment = Comment.objects.create(
            author="anon",
            text="test"
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.comment.author, str)
        self.assertIsInstance(self.comment.text, str)
