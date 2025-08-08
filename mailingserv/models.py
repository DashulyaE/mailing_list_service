from django.db import models

class Client(models.Model):
    """Модель 'Получатель рассылки' """
    email = models.EmailField(verbose_name="Email")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"

    def __str__(self):
        return f"{self.full_name}, {self.email}"


class Message(models.Model):
    """Модель 'Сообщение' """
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(verbose_name="Тело письма", help_text='Введите текст сообщения')

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"

    def __str__(self):
        return self.subject