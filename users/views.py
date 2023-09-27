from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetCompleteView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView

from users.forms import UserForm, UserRegisterForm, CustomPasswordResetForm, CustomResetConfirmForm
from users.models import User


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:index')


class CustomPasswordResetView(PasswordResetView):
    template_name = 'users/password_reset_form.html'
    form_class = CustomPasswordResetForm

    def form_valid(self, form):
        uid, token = form.save(self.request)
        return redirect('users:password_reset_confirm', uidb64=uid, token=token)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomResetConfirmForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'users/password_reset_complete.html'
