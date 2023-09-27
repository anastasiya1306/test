from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from users.models import User


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, UserChangeForm):
    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'avatar')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    phone = forms.CharField(
        max_length=25,
        required=True,
        label="Номер телефона",
        widget=forms.TextInput(attrs={'placeholder': 'Номер телефона'}),
    )

    class Meta:
        model = User
        fields = ('phone', 'password1', 'password2')

    def clean_phone(self):
        """
            Проверка номера телефона на уникальность.
        """
        phone = self.cleaned_data.get('phone')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError("Пользователь с таким номером уже существует")
        return phone

    def save(self, commit=True):
        """
            Сохранение пользователя.
        """

        user = super().save(commit=False)
        user.phone = self.cleaned_data["phone"]
        if commit:
            user.save()
        return user


class CustomPasswordResetForm(StyleFormMixin, PasswordResetForm):
    email = forms.EmailField(
        widget=forms.HiddenInput(),
        required=False,
    )

    phone = forms.CharField(
        label=("Номер телефона"),
        max_length=254,
        widget=forms.TextInput(attrs={"autocomplete": "phone"}),
    )

    def save(self, request, **kwargs):
        phone = self.cleaned_data["phone"]
        user = User.objects.get(phone=phone)

        token_generator = kwargs.get('token_generator', default_token_generator)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)

        return uid, token


class CustomResetConfirmForm(SetPasswordForm):
    class Meta:
        model = User
