from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class UserProfileView(LoginRequiredMixin, DetailView):
    """Контроллер просмотра профиля пользователя"""
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        # Возвращает текущего залогиненного пользователя
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя"""

    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:user_profile')  # перенаправление на страницу профиля

    def get_object(self):
        # Возвращает текущего пользователя
        return self.request.user