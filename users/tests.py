from django.test import TestCase
from django.urls import reverse

from users.models import User


class SetupTestCase(TestCase):

    def setUp(self):
        self.user = User(
            phone='79532815720',
            avatar='skypro.png',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )
        self.user.set_password('qwe123rty')
        self.user.save()


class LoginViewTest(SetupTestCase):

    def test_login_page(self):
        url = reverse('users:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login(self):
        url = reverse('users:login')
        test = {
            'username': '79532815720',
            'password': 'qwe123rty'
        }
        response = self.client.post(url, test)
        self.assertEqual(response.status_code, 302)


class ProfileUpdateViewTest(SetupTestCase):

    def setUp(self):
        super().setUp()
        self.url = reverse('users:profile')
        self.client.login(username='79532815720', password='qwe123rty')

    def test_profile_update_view(self):
        test = {
            'phone': '79532815720',
            'avatar': 'skypro.png',
        }
        self.client.post(self.url, test)
        self.assertEqual(self.user.phone, '79532815720')
        self.assertEqual(self.user.avatar, 'skypro.png')


