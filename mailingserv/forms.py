from django.forms import ModelForm, BooleanField

from mailingserv.models import Mailing, Client, Message


class StyleFormMixin:
    """Класс со стилями для форм"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for fild_name, fild in self.fields.items():
            if isinstance(fild, BooleanField):
                fild.widget.attrs["class"] = "form-check-input"
            else:
                fild.widget.attrs["class"] = "form-control"


class MailingForm(StyleFormMixin, ModelForm):
    """Класс для создания формы для рассылки"""

    class Meta:
        model = Mailing
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_datetime")
        end = cleaned_data.get("end_datetime")
        if start and end and start >= end:
            self.add_error(
                "start_datetime", "Дата начала должна быть раньше даты окончания."
            )
        return cleaned_data


class ClientForm(StyleFormMixin, ModelForm):
    """Класс для создания формы для получателей"""

    class Meta:
        model = Client
        fields = "__all__"


class MessageForm(StyleFormMixin, ModelForm):
    """Класс для создания формы для сообщений"""

    class Meta:
        model = Message
        fields = "__all__"
