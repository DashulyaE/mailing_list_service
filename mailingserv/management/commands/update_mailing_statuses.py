from django.core.management.base import BaseCommand
from django.utils import timezone
from mailingserv.models import Mailing

class Command(BaseCommand):
    help = 'Обновление статусов рассылок в зависимости от времени'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        mailings = Mailing.objects.all()

        for mailing in mailings:
            if mailing.status != 'finished':
                if now > mailing.end_datetime:
                    mailing.status = 'finished'
                    mailing.save()
                    self.stdout.write(f"Рассылка {mailing.id} завершена.")
                elif mailing.start_datetime <= now <= mailing.end_datetime:
                    mailing.status = 'started'
                    mailing.save()
                    self.stdout.write(f"Рассылка {mailing.id} запущена.")