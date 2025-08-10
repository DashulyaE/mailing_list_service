from django.contrib import admin

from mailingserv.models import Client, Message, Mailing, Attempt


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("id", "full_name", "comment")
    list_filter = ("email", "full_name")
    search_fields = ("email", "full_name")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "subject",
    )
    list_filter = ("subject",)
    search_fields = ("subject",)


@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "start_datetime",
        "status",
        "message_subject",
        "clients_count",
    )
    search_fields = ("status", "message_subject")
    list_filter = ("status", "start_datetime")

    def message_subject(self, obj):
        return obj.message.subject

    message_subject.short_description = "Тема письма"

    def clients_count(self, obj):
        return obj.clients.count()

    clients_count.short_description = "Кол-во получателей"


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "mailing",
        "attempt_datetime",
        "status",
        "server_response",
    )
    search_fields = ("status", "server_response", "mailing__message__subject")
    list_filter = ("status", "attempt_datetime")
