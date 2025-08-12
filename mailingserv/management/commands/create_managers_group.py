from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from users.models import User
from mailingserv.models import Client, Mailing, Message

class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        # Создаем или получаем группу "Менеджеры"
        group, created = Group.objects.get_or_create(name='Менеджеры')
        if created:
            self.stdout.write('Группа "Менеджеры" создана')
        else:
            self.stdout.write('Группа "Менеджеры" уже существует')

        # Получаем права для моделей
        content_type_client = ContentType.objects.get_for_model(Client)
        content_type_mailing = ContentType.objects.get_for_model(Mailing)
        content_type_message = ContentType.objects.get_for_model(Message)
        content_type_user = ContentType.objects.get_for_model(User)

        # Назначаем права для группы "Менеджеры"
        permissions = Permission.objects.filter(
            content_type__in=[
                content_type_client,
                content_type_mailing,
                content_type_message,
                content_type_user,
            ],
            codename__in=[
                'can_view_client',          # Просмотр клиентов
                'can_view_all_mailing',         # Просмотр рассылок
                'can_view_message',         # Просмотр сообщений
                'can_view_user',            # Просмотр пользователей
                'can_block_user',       # Блокировка пользователей
                'can_finish_mailing',   # Отключение рассылок
            ]
        )

        group.permissions.set(permissions)
        self.stdout.write('Права назначены группе "Менеджеры"')