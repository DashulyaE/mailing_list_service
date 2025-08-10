from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from mailingserv.forms import MailingForm
from mailingserv.models import Mailing, Client


class MailingHomeView(TemplateView):
    template_name = "mailingserv/home.html"
    context_object_name = "home"


class MailinglistView(ListView):
    model = Mailing


class MailingDetailView(DetailView):
    model = Mailing


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailingserv:mailing_list")


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailingserv:mailing_list")


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy("mailingserv:mailing_list")


class ClientlistView(ListView):
    model = Client

