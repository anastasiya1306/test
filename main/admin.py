from django.contrib import admin

from main.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'blog', 'user', 'status', 'payment_status', 'payment_date',)
