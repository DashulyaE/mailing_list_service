from django.core.mail import send_mail
from django.utils import timezone

from config import settings
from mailingserv.models import Attempt, Client


class MailingSender:
    """Класс для отправки рассылки и охранения попытки рассылки"""

    def __init__(self, mailing):
        self.mailing = mailing
        self.attempts = []

    def send(self):
        success_count = 0
        total_recipients = self.mailing.clients.count()

        recipients = self.mailing.clients.all()
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
        self.mailing.status = "finished"
        self.mailing.save()

        return self.attempts
