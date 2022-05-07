from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from app_users.models import Profile


class RegisterPageTest(TestCase):
    def test_register_page(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_register_exists_at_desired_location(self):
        response = self.client.get('/users/register/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_post(self):
        response = self.client.post('/users/register/', {'username': 'testuser', 'password1': 'testpassword123', 'password2': 'testpassword123'})
        self.assertRedirects(response, '/')


class LoginPageTest(TestCase):
    def test_logged_in(self):
        user = User.objects.create(
            first_name="test",
            last_name="test",
            username="test",
            password="16051998q",
        )

        response = self.client.post('/users/login/', {'username': user.username, 'password': user.password})
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_exists_at_desired_location(self):
        response = self.client.get('/users/login/')
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'users/login.html')


class ProfilePageTest(TestCase):
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

    def test_profile_page(self):
        logged_in = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/users/{self.profile.user.id}/')

        self.assertTrue(logged_in)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')


class ProfileEditPageTest(TestCase):
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

    def test_profile_edit_page(self):
        logged_in = self.client.login(username='testuser', password='12345')
        response = self.client.get(f'/users/{self.profile.user.id}/edit/')

        self.assertTrue(logged_in)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile_edit.html')
