from django.urls import reverse

from blog.models import Blog
from main.models import Subscription
from users.tests import SetupTestCase


class SubscriptionViewTest(SetupTestCase):

    def setUp(self):
        super().setUp()
        self.blog = Blog.objects.create(title='Blog1')
        self.subscription = Subscription.objects.create(
            user=self.user,
            blog=self.blog
        )

    def test_create_view(self):
        self.client.login(phone='79532815720', password='qwe123rty')
        url = reverse('main:subscription_create', args=[self.blog.slug])
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)

    def test_delete_view(self):
        self.client.login(phone='79532815720', password='qwe123rty')
        url = reverse('main:subscription_delete', args=[self.subscription.blog.slug])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)


class SubscriptionListViewTest(SetupTestCase):

    def test_subscription_list_view(self):
        self.client.login(phone='79532815720', password='qwe123rty')
        response = self.client.get(reverse('main:subscription_list'))
        self.assertEqual(response.status_code, 200)


class SuccessViewTest(SetupTestCase):
    def setUp(self):
        super().setUp()
        self.blog = Blog.objects.create(title='Blog1', payment_amount=2)
        self.url = reverse('main:success', kwargs={'slug': self.blog.slug})

    def test_success_view(self):
        self.client.login(phone='79532815720', password='qwe123rty')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)