from django.urls import path, include
from mailingserv.apps import MailingservConfig
from mailingserv.views import MailinglistView, MailingDetailView, MailingHomeView

app_name = MailingservConfig.name

urlpatterns = [
    path("", MailingHomeView.as_view(), name="home"),
    path("mailingserv/", MailinglistView.as_view(), name="mailing_list"),
    path("mailingserv/<int:pk>", MailingDetailView.as_view(), name="mailing_detail"),
]
