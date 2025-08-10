from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
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
from mailingserv.models import Mailing, Client, Message
from mailingserv.services import check_and_update_mailings


class MailingHomeView(TemplateView):
    template_name = "mailingserv/home.html"
    context_object_name = "home"


class MailinglistView(ListView):
    model = Mailing

    def get_queryset(self):
        check_and_update_mailings()
        return super().get_queryset()


class MailingDetailView(DetailView):
    model = Mailing

    def get(self, request, *args, **kwargs):
        check_and_update_mailings()
        return super().get(request, *args, **kwargs)

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
    """Отправка рассылки вручную с сайта"""
    mailing = get_object_or_404(Mailing, pk=pk)
    recipients = mailing.clients.all()
    for client in recipients:
        send_mail(
            subject=mailing.message.subject,
            message=mailing.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[client.email],
        )
    # Обновляем статус
    mailing.status = 'started'
    mailing.save()
    messages.success(request, "Рассылка отправлена вручную.")
    return redirect('mailingserv:mailing_detail', pk=pk)