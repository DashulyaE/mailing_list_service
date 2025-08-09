from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from mailingserv.models import Mailing


class MailingHomeView(TemplateView):
    template_name = "mailingserv/home.html"
    context_object_name = "home"


class MailinglistView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing