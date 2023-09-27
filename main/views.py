import json
from django.conf import settings
from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.views import View
import stripe
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.http import JsonResponse, HttpResponse

from blog.models import Blog
from main.forms import SubscriptionForm
from django.views.generic import DeleteView, ListView, TemplateView, CreateView
from main.models import Subscription
from users.models import User

stripe.api_key = settings.STRIPE_SECRET_KEY
DOMAIN = "http://127.0.0.1:8000"


class CreateCheckoutSessionView(View):

    def post(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])

        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': blog.payment_amount * 100,
                            'product_data': {
                                'name': blog.title,
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=DOMAIN + reverse('main:success', kwargs={'slug': blog.slug}),
                cancel_url=DOMAIN + reverse('main:cancel')
            )

        return redirect(checkout_session.url, code=303)


class CancelView(TemplateView):
    template_name = 'main/cancel.html'


class SuccessView(TemplateView):
    template_name = 'main/success.html'

    def get(self, request, *args, **kwargs):
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        user = self.request.user

        Subscription.objects.create(
            user=user,
            blog=blog,
            status=True,
            payment_status=True,
            payment_date=timezone.now()
        )
        return render(request, 'main/success.html')


class SubscriptionCreateView(CreateView):
    model = Subscription
    template_name = 'main/subscription_form.html'
    success_url = reverse_lazy('blog:blog_list')
    form_class = SubscriptionForm

    def form_valid(self, form):

        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        form.create_subscription(self.request.user, blog)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        blog = get_object_or_404(Blog, slug=self.kwargs['slug'])
        context['blog'] = blog
        return context


class SubscriptionListView(ListView):
    model = Subscription
    template_name = 'main/subscription_list.html'

    def get_queryset(self):
        user = self.request.user

        subscription_blogs_id = Subscription.objects.filter(user=user, status=True).values_list('blog__id', flat=True)
        subscription_blogs = Blog.objects.filter(id__in=subscription_blogs_id, is_publication=True)
        user_blog_publication = Blog.objects.filter(user=user, is_publication=True)
        user_blog_unpublication = Blog.objects.filter(user=user, is_publication=False)
        data = (subscription_blogs | user_blog_publication | user_blog_unpublication).distinct()

        return data


class SubscriptionDeleteView(DeleteView):
    model = Subscription
    template_name = 'main/subscription_confirm_delete.html'
    success_url = reverse_lazy('main:subscription_list')

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    def get_object(self, queryset=None):
        return get_object_or_404(self.get_queryset(), blog__slug=self.kwargs['slug'])
