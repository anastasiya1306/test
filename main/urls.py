from main.apps import MainConfig
from django.urls import path

from main.views import CancelView, \
    SuccessView, CreateCheckoutSessionView, SubscriptionCreateView, SubscriptionDeleteView, \
    SubscriptionListView

app_name = MainConfig.name

urlpatterns = [
    path('subscription-create/<slug:slug>/', SubscriptionCreateView.as_view(), name='subscription_create'),
    path('subscription-cancel/<slug:slug>/', SubscriptionDeleteView.as_view(), name='subscription_delete'),
    path('subscription-list/', SubscriptionListView.as_view(), name='subscription_list'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/<slug:slug>/', SuccessView.as_view(), name='success'),
    path('create-checkout-session/<slug:slug>/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
]
