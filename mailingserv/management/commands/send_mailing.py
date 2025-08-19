from django.core.management.base import BaseCommand
from mailingserv.models import Mailing
from django.core.mail import send_mail
from django.conf import settings


class Command(BaseCommand):
    help = "Отправка рассылки по ID"

    def add_arguments(self, parser):
        parser.add_argument("pk", type=int, help="ID рассылки")

    def handle(self, *args, **kwargs):
        pk = kwargs["pk"]
        mailing = Mailing.objects.get(pk=pk)
        mailing.status = "started"
        mailing.save()
        recipients = mailing.clients.all()

        for client in recipients:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
            )
        self.stdout.write(f"Рассылка {pk} отправлена успешно.")
