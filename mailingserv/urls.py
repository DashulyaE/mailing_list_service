from django.urls import path, include
from mailingserv.apps import MailingservConfig
from mailingserv.views import home

app_name = MailingservConfig.name

urlpatterns = [
    path('', home, name='home'),
]