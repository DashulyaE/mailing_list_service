from django.utils import timezone
from mailingserv.models import Mailing

def check_and_update_mailings():
    """Изменения статуса рассылки"""
    now = timezone.now()
    mailings_to_update = Mailing.objects.filter(status='started', end_datetime__lt=now)
    for mailing in mailings_to_update:
        mailing.status = 'finished'
        mailing.save()