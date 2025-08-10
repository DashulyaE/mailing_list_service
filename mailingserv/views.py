from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    TemplateView,
    CreateView,
    UpdateView,
    DeleteView,
)

from config import settings
from mailingserv.forms import MailingForm, ClientForm, MessageForm
from mailingserv.models import Mailing, Client, Message, Attempt
from mailingserv.services import MailingSender


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
    form_class = MessageForm
    success_url = reverse_lazy("mailingserv:message_list")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailingserv:message_list")


class MessageDeleteView(DeleteView):
    model = Message
    success_url = reverse_lazy("mailingserv:message_list")


def send_newmailing(request, pk):
    """Контроллер для отображения попытки рассылки"""
    mailing = get_object_or_404(Mailing, pk=pk)
    sender = MailingSender(mailing)
    attempts = sender.send()
    return render(
        request,
        "mailingserv/mailing_attempts.html",
        {
            "mailing": mailing,
            "attempts": attempts,
        },
    )


def all_attempts_list(request):
    """Контроллер для записи всех попыток рассылок в шаблон"""
    attempts = Attempt.objects.select_related("mailing").all()
    return render(request, "mailingserv/mailing_attempts.html", {"attempts": attempts})
