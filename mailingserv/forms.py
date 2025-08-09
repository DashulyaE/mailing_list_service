from django.forms import ModelForm

from mailingserv.models import Mailing


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"