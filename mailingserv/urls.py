
from django.urls import path, include
from django.views.decorators.cache import cache_page

from mailingserv import views
from mailingserv.apps import MailingservConfig
from mailingserv.views import (
    MailinglistView,
    MailingDetailView,
    MailingHomeView,
    MailingCreateView,
    MailingUpdateView,
    MailingDeleteView,
    ClientlistView,
    ClientDetailView,
    ClientCreateView,
    ClientUpdateView,
    ClientDeleteView,
    MessagelistView,
    MessageDetailView,
    MessageCreateView,
    MessageUpdateView,
    MessageDeleteView,
    send_newmailing, user_report, MailingUpdateModeratorView
)

app_name = MailingservConfig.name

urlpatterns = [
    path("", MailingHomeView.as_view(), name="home"),
    path("mailing/", MailinglistView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>", cache_page(60)(MailingDetailView.as_view()), name="mailing_detail"),
    path("mailing/create", MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"
    ),
    path(
        "mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"
    ),
    path("client/", ClientlistView.as_view(), name="client_list"),
    path("client/<int:pk>", cache_page(60)(ClientDetailView.as_view()), name="client_detail"),
    path("client/create", ClientCreateView.as_view(), name="client_create"),
    path("client/<int:pk>/update/", ClientUpdateView.as_view(), name="client_update"),
    path("client/<int:pk>/delete/", ClientDeleteView.as_view(), name="client_delete"),
    path("message/", MessagelistView.as_view(), name="message_list"),
    path("message/<int:pk>", cache_page(60)(MessageDetailView.as_view()), name="message_detail"),
    path("message/create", MessageCreateView.as_view(), name="message_create"),
    path("message/<int:pk>/update/", MessageUpdateView.as_view(), name="message_update"),
    path("message/<int:pk>/delete/", MessageDeleteView.as_view(), name="message_delete"),
    path("mailing/<int:pk>/send/", send_newmailing, name="mailing_send"),
    path("mailing/all_attempts/", views.all_attempts_list, name="all_attempts"),
    path('user-report/', user_report, name='user_report'),
    path(
        "mailing/<int:pk>/update_mod/", MailingUpdateModeratorView.as_view(), name="mailing_update_moderator"
    ),
]
