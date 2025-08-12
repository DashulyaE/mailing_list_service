from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, ListView

from users.forms import UserRegisterForm, UserUpdateForm
from users.models import User


class RegisterView(CreateView):
    """Регистрация пользователя"""

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
        return self.request.user


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Контроллер редактирования профиля пользователя"""

    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile_edit.html'
    success_url = reverse_lazy('users:user_profile')

    def get_object(self):
        return self.request.user


class CustomPasswordResetView(PasswordResetView):
    template_name = "users/password_reset_form.html"
    email_template_name = "users/password_reset_email.html"
    subject_template_name = "users/password_reset_subject.txt"
    success_url = "/users/password_reset/done/"


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "users/password_reset_done.html"


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = "users/password_reset_confirm.html"
    success_url = "/users/reset/done/"


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = "users/password_reset_complete.html"


class UserListView(LoginRequiredMixin, ListView):
    """Список пользователей"""

    model = User
    template_name = "messaging/user_list.html"
    context_object_name = "users"


class CustomLoginView(LoginView):
    """Кастомный класс, который проверяет статус блокировки"""

    def form_valid(self, form):
        user = form.get_user()
        if user.is_blocked:
            messages.error(self.request, "Ваш аккаунт заблокирован.")
            return self.form_invalid(form)
        return super().form_valid(form)


class UserBlockToggleView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Класс блокировки пользователя"""

    model = User
    fields = ['is_blocked']
    template_name = 'users/block_toggle.html'
    success_url = reverse_lazy('users:user_list')

    def test_func(self):
        return self.request.user.is_superuser  # или другая проверка

    def get_object(self, queryset=None):
        user_id = self.kwargs['pk']
        return User.objects.get(pk=user_id)
