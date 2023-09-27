from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from django.urls import path

from users.views import ProfileUpdateView, RegisterView, CustomPasswordResetView, CustomPasswordResetConfirmView, \
    CustomPasswordResetCompleteView

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password/reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/confirm/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password/reset/complete/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]