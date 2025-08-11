from django.contrib.auth.forms import UserCreationForm
from django import forms

from mailingserv.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """Класс для создания формы регистрации поользователя"""

    class Meta:
        model = User
        fields = ("email", "password1", "password2")


class UserUpdateForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'phone', 'country', 'avatar']