from django.urls import path, include
from mailingserv.apps import MailingservConfig
from mailingserv.views import MailinglistView, MailingDetailView, MailingHomeView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView

app_name = MailingservConfig.name

urlpatterns = [
    path("", MailingHomeView.as_view(), name="home"),
    path("mailingserv/", MailinglistView.as_view(), name="mailing_list"),
    path("mailingserv/<int:pk>", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailingserv/create", MailingCreateView.as_view(), name="mailing_create"),
    path("mailingserv/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailingserv/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
]
