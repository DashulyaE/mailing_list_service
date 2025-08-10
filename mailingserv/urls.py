from django.urls import path, include
from mailingserv.apps import MailingservConfig
from mailingserv.views import MailinglistView, MailingDetailView, MailingHomeView, MailingCreateView, MailingUpdateView, \
    MailingDeleteView, ClientlistView

app_name = MailingservConfig.name

urlpatterns = [
    path("", MailingHomeView.as_view(), name="home"),
    path("mailing/", MailinglistView.as_view(), name="mailing_list"),
    path("mailing/<int:pk>", MailingDetailView.as_view(), name="mailing_detail"),
    path("mailing/create", MailingCreateView.as_view(), name="mailing_create"),
    path("mailing/<int:pk>/update/", MailingUpdateView.as_view(), name="mailing_update"),
    path("mailing/<int:pk>/delete/", MailingDeleteView.as_view(), name="mailing_delete"),
    path("client/", ClientlistView.as_view(), name="client_list"),
]
