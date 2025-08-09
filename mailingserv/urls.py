from django.urls import path, include
from mailingserv.apps import MailingservConfig
from mailingserv.views import mailing_list

app_name = MailingservConfig.name

urlpatterns = [
    path("", mailing_list, name="base"),
]
