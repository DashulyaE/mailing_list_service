from django.contrib import admin

from mailingserv.models import Client, Message, Mailing


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "comment")
    list_filter = ("email",)
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "subject",)
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = ("id", "start_datetime", "status", "message_subject", "clients_count")
    search_fields = ("status", "message_subject")
    list_filter = ("status", "start_datetime")

    def message_subject(self, obj):
        return obj.message.subject

    message_subject.short_description = "Тема письма"

    def clients_count(self, obj):
        return obj.clients.count()

    clients_count.short_description = "Кол-во получателей"