from django.test import TestCase
from django.urls import reverse
from app_users.models import Profile
from django.contrib.auth.models import User


class ProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            first_name="test",
            last_name="test",
            username="test",
            password="16051998q",
        )

        cls.profile = Profile.objects.create(
            user=user,
            city="moscow",
            phone="555",
            is_verified=False,
            news_count=0
        )

    def test_it_has_information_fields(self):
        self.assertIsInstance(self.profile.user.id, int)
        self.assertIsInstance(self.profile.user.first_name, str)
        self.assertIsInstance(self.profile.user.last_name, str)
        self.assertIsInstance(self.profile.user.username, str)
        self.assertIsInstance(self.profile.user.password, str)

        self.assertIsInstance(self.profile.city, str)
        self.assertIsInstance(self.profile.phone, str)
        self.assertIsInstance(self.profile.is_verified, bool)
        self.assertIsInstance(self.profile.news_count, int)

