from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, UserProfileView, UserProfileUpdateView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('profile/edit/', UserProfileUpdateView.as_view(), name='user_profile_edit')
]