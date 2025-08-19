from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
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

from mailingserv import services
from mailingserv.forms import MailingForm, ClientForm, MessageForm, MailingModeratorForm
from mailingserv.models import Mailing, Client, Message, Attempt
from mailingserv.services import (
    MailingSender,
    get_statistics,
    get_mailing_cache,
    get_сlient_cache,
    get_message_cache,
)
from users.models import User


class MailingHomeView(TemplateView):
    template_name = "mailingserv/home.html"
    context_object_name = "home"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(
            name="Менеджеры"
        ).exists()
        context.update(get_statistics())
        return context


class MailinglistView(ListView, LoginRequiredMixin):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(
            name="Менеджеры"
        ).exists()
        return context

    def get_queryset(self):
        mailing_qs = get_mailing_cache()
        user = self.request.user
        if not user.groups.filter(name="Менеджеры").exists():
            mailing_qs = mailing_qs.filter(owner=user)
        return mailing_qs


class MailingDetailView(DetailView, LoginRequiredMixin):
    model = Mailing


class MailingCreateView(CreateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailingserv:mailing_list")

    def form_valid(self, form):
        mailing = form.save(commit=False)
        mailing.owner = self.request.user
        mailing.save()
        return super().form_valid(form)


class MailingUpdateView(UpdateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy("mailingserv:mailing_list")


class MailingUpdateModeratorView(UpdateView, LoginRequiredMixin):
    model = Mailing
    form_class = MailingModeratorForm
    success_url = reverse_lazy("mailingserv:mailing_list")


class MailingDeleteView(DeleteView, LoginRequiredMixin):
    model = Mailing
    success_url = reverse_lazy("mailingserv:mailing_list")


class ClientlistView(ListView, LoginRequiredMixin):
    model = Client

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(
            name="Менеджеры"
        ).exists()
        return context

    def get_queryset(self):
        сlient_qs = get_сlient_cache()
        user = self.request.user
        if not user.groups.filter(name="Менеджеры").exists():
            сlient_qs = сlient_qs.filter(owner=user)
        return сlient_qs


class ClientDetailView(DetailView, LoginRequiredMixin):
    model = Client


class ClientCreateView(CreateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailingserv:client_list")

    def form_valid(self, form):
        client = form.save(commit=False)
        client.owner = self.request.user
        client.save()
        return super().form_valid(form)


class ClientUpdateView(UpdateView, LoginRequiredMixin):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy("mailingserv:client_list")


class ClientDeleteView(DeleteView, LoginRequiredMixin):
    model = Client
    success_url = reverse_lazy("mailingserv:client_list")


class MessagelistView(ListView, LoginRequiredMixin):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_manager"] = self.request.user.groups.filter(
            name="Менеджеры"
        ).exists()
        return context

    def get_queryset(self):
        message_qs = get_message_cache()
        user = self.request.user
        if not user.groups.filter(name="Менеджеры").exists():
            message_qs = message_qs.filter(owner=user)
        return message_qs


class MessageDetailView(DetailView, LoginRequiredMixin):
    model = Message


class MessageCreateView(CreateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailingserv:message_list")

    def form_valid(self, form):
        message = form.save(commit=False)
        message.owner = self.request.user
        message.save()
        return super().form_valid(form)


class MessageUpdateView(UpdateView, LoginRequiredMixin):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy("mailingserv:message_list")


class MessageDeleteView(DeleteView, LoginRequiredMixin):
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
    is_manager = request.user.groups.filter(name="Менеджеры").exists()
    return render(
        request,
        "mailingserv/mailing_attempts.html",
        {
            "attempts": attempts,
            "is_manager": is_manager,
        },
    )


@login_required
def user_report(request):
    """Формирует данные по статистике и передает их в шаблон"""
    users = User.objects.all()
    user_stats = []

    for user in users:
        stats = {
            "user": user,
            "successful_attempts": services.get_successful_attempts_count(user),
            "failed_attempts": services.get_failed_attempts_count(user),
            "messages_sent": services.get_sent_messages_count(user),
        }
        user_stats.append(stats)

    is_manager = request.user.groups.filter(name="Менеджеры").exists()
    return render(
        request,
        "mailingserv/user_report.html",
        {
            "user_stats": user_stats,
            "is_manager": is_manager,
        },
    )


@login_required
@permission_required("mailingserv.change_mailing")
def edit_mailing_subscription(request, pk):
    """переопределяет форму для редактирования рассылок в зависимости от прав пользователя"""
    mailing = get_object_or_404(Mailing, pk=pk)
    if request.method == "POST":
        form = MailingForm(request.POST, instance=mailing)
        if form.is_valid():
            form.save()
            return redirect("mailingserv:mailing_list")
    else:
        form = MailingForm(instance=mailing)
    return render(
        request, "mailingserv/edit_mailing.html", {"form": form, "mailing": mailing}
    )
