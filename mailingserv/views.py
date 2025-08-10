from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView

from mailingserv.forms import MailingForm, ClientForm, MessageForm
from mailingserv.models import Mailing, Client, Message


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


class ClientDetailView(DetailView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailingserv:client_list")


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailingserv:client_list")


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mailingserv:client_list")


class MessagelistView(ListView):
    model = Message


class MessageDetailView(DetailView):
    model = Message


class MessageCreateView(CreateView):
    model = Message
    form_class = ClientForm
    success_url = reverse_lazy("mailingserv:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailingserv:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailingserv:message_list")