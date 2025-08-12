from django.db import models

from users.models import User


class Client(models.Model):
    """Модель 'Получатель рассылки'"""

    email = models.EmailField(verbose_name="Email", unique=True)
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    comment = models.TextField(verbose_name="Комментарий", blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )
    is_subscribed = models.BooleanField(
        default=True, verbose_name="Подписан на рассылку"
    )

    class Meta:
        verbose_name = "Получатель"
        verbose_name_plural = "Получатели"
        permissions = [
            ("can_view_client", "Может видеть список клиентов"),
        ]

    def __str__(self):
        return f"{self.full_name}, {self.email}"


class Message(models.Model):
    """Модель 'Сообщение'"""

    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    body = models.TextField(
        verbose_name="Тело письма", help_text="Введите текст сообщения"
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        permissions = [
            ("can_view_message", "Может видеть список сообщений"),
        ]

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Модель 'Рассылка'"""

    STATUS_CHOICES = [
        ("created", "Создана"),
        ("started", "Запущена"),
        ("finished", "Завершена"),
    ]

    start_datetime = models.DateTimeField(verbose_name="Дата и время первой отправки")
    end_datetime = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="created", verbose_name="Статус"
    )
    message = models.ForeignKey(
        Message, on_delete=models.CASCADE, verbose_name="Сообщение"
    )
    clients = models.ManyToManyField(
        Client, related_name="newsletters", verbose_name="Получатели"
    )
    is_active = models.BooleanField(default=True, verbose_name="Активна")
    is_subscribed = models.BooleanField(default=True, verbose_name="Включена")
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Владелец", null=True
    )

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        permissions = [
            ("can_view_all_mailing", "Может видеть все рассылки"),
            ("can_finish_mailing", "Может отключить рассылку"),
        ]

    def __str__(self):
        return f"Рассылка {self.id} - {self.get_status_display()}"


class Attempt(models.Model):
    """Попытка рассылки"""

    SUCCESS = "success"
    FAILURE = "failure"

    STATUS_CHOICES = [
        (SUCCESS, "Успешно"),
        (FAILURE, "Не успешно"),
    ]
    attempt_datetime = models.DateTimeField(verbose_name="Дата и время попытки")
    mailing = models.ForeignKey(
        Mailing, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, verbose_name="Статус попытки"
    )
    server_response = models.TextField(
        blank=True, null=True, verbose_name="Ответ сервера"
    )

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"

    def __str__(self):
        return f"Попытка {self.id} - {self.get_status_display()}"
