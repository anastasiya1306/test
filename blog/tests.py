from django.urls import reverse
from blog.models import Blog
from users.tests import SetupTestCase


class BlogViewTests(SetupTestCase):

    def setUp(self):
        super().setUp()

        self.client.login(phone='79532815720', password='qwe123rty')


class BlogListViewTest(SetupTestCase):

    def test_list_blog(self):
        Blog.objects.create(title='Blog1', description='Test1', is_publication=True)
        Blog.objects.create(title='Blog2', description='Test2', is_publication=True)

        url = reverse('blog:blog_list')
        self.client.login(phone='79532815720', password='qwe123rty')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class BlogDetailViewTest(SetupTestCase):

    def test_detail_blog(self):
        blog = Blog.objects.create(title='Blog1')
        url = reverse('blog:blog_detail', args=[blog.slug])
        self.client.login(phone='79532815720', password='qwe123rty')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class BlogUpdateViewTest(SetupTestCase):

    def setUp(self):
        super().setUp()
        self.blog = Blog.objects.create(title='Blog1', description='Test1')
        self.url = reverse('blog:blog_update', args=[self.blog.pk])

    def test_update_blog_authenticate(self):
        self.client.login(phone='79532815720', password='qwe123rty')

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        test = {
            'title': 'Blog 1',
            'description': 'Test 1',
            'payment_amount': 3,
            'is_paid': True,
        }

        response = self.client.post(self.url, test)
        self.assertEqual(response.status_code, 302)

        updated_blog = Blog.objects.get(pk=self.blog.pk)
        self.assertEqual(updated_blog.title, 'Blog 1')
        self.assertEqual(updated_blog.description, 'Test 1')

    def test_update_blog_unauthenticate(self):
        response = self.client.post(self.url, {'title': 'Blog 1', 'description': 'Test 1'})
        self.assertEqual(response.status_code, 302)

        updated_blog = Blog.objects.get(pk=self.blog.pk)
        self.assertEqual(updated_blog.title, 'Blog1')
        self.assertEqual(updated_blog.description, 'Test1')


class BlogDeleteViewTest(SetupTestCase):

    def setUp(self):
        super().setUp()
        self.blog = Blog.objects.create(title='Blog1', description='Test1')
        self.url = reverse('blog:blog_delete', args=[self.blog.pk])

    def test_delete_blog(self):
        self.client.login(phone='79532815720', password='qwe123rty')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
