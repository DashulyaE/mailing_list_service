from django.forms import ModelForm

from mailingserv.models import Mailing, Client, Message


class MailingForm(ModelForm):
    class Meta:
        model = Mailing
        fields = "__all__"


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = "__all__"