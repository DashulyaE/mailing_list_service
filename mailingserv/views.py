from django.shortcuts import render

from mailingserv.models import Mailing


def mailing_list(request):
    mailings = Mailing.objects.all()
    context = {"mailings":mailings}
    return render(request, "mailingserv/mailings_list.html", context)
