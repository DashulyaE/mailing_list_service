from django.core.cache import cache
from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from config.settings import CACHE_ENABLED
from mailingserv.models import Attempt, Client, Mailing, Message


class MailingSender:
    """Класс для отправки рассылки и cохранения попытки рассылки"""

    def __init__(self, mailing):
        self.mailing = mailing
        self.attempts = []

    def send(self):
        self.mailing.status = "created"
        self.mailing.save()
        success_count = 0
        total_recipients = self.mailing.clients.filter(is_subscribed=True).count()

        recipients = self.mailing.clients.filter(is_subscribed=True)
        for client in recipients:
            try:
                if not Client.objects.filter(email=client.email).exists():
                    raise Exception("Клиент с таким email не существует")
                result = send_mail(
                    subject=self.mailing.message.subject,
                    message=self.mailing.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[client.email],
                )
                if result > 0:
                    status = Attempt.SUCCESS
                    server_response = "Письмо успешно отправлено"
                    success_count += 1
                else:
                    status = Attempt.FAILURE
                    server_response = "Письмо не отправлено"
            except Exception as e:
                status = Attempt.FAILURE
                server_response = str(e)

            attempt = Attempt.objects.create(
                attempt_datetime=timezone.now(),
                mailing=self.mailing,
                status=status,
                server_response=server_response,
            )
            self.attempts.append(attempt)

        if success_count == total_recipients:
            self.mailing.overall_status = "success"
        else:
            self.mailing.overall_status = "failure"
        self.mailing.status = "started"
        self.mailing.save()

        return self.attempts


def get_statistics():
    total_mailings = Mailing.objects.count()
    active_mailings = Mailing.objects.filter(status="started").count()
    unique_recipients = (
        Client.objects.filter(newsletters__isnull=False).distinct().count()
    )
    total_attempts = Attempt.objects.count()

    return {
        "total_mailings": total_mailings,
        "active_mailings": active_mailings,
        "unique_recipients": unique_recipients,
        "total_attempts": total_attempts,
    }


def get_successful_attempts_count(user):
    return Attempt.objects.filter(mailing__owner=user, status=Attempt.SUCCESS).count()


def get_failed_attempts_count(user):
    return Attempt.objects.filter(mailing__owner=user, status=Attempt.FAILURE).count()


def get_sent_messages_count(user):
    return Message.objects.filter(mailing__owner=user).count()


def get_mailing_cache():
    """Получает данные по рассылкам из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Mailing.objects.all()
    key = "mailing_list"
    mailing = cache.get(key)
    if mailing is not None:
        return mailing
    mailing = Mailing.objects.all()
    cache.set(key, mailing)
    return mailing


def get_сlient_cache():
    """Получает данные по получателям из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Client.objects.all()
    key = "сlient_list"
    сlient = cache.get(key)
    if сlient is not None:
        return сlient
    сlient = Client.objects.all()
    cache.set(key, сlient)
    return сlient


def get_message_cache():
    """Получает данные по сообщениям из кэша, если кэш пуст, получает данные из БД"""
    if not CACHE_ENABLED:
        return Message.objects.all()
    key = "message_list"
    message = cache.get(key)
    if message is not None:
        return message
    message = Message.objects.all()
    cache.set(key, message)
    return message
