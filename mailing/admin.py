from django.contrib import admin

from .models import MailingAttempt, MailingUnit, MailReceiver, Message


@admin.register(MailReceiver)
class MailReceiverAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")
    search_fields = ("email", "full_name", "comment")


@admin.register(MailingUnit)
class MailingUnitAdmin(admin.ModelAdmin):
    list_display = ("message", "status", "started_at", "finished_at", "get_receivers")
    list_filter = ["status"]
    search_fields = ("status", "get_receivers")
    exclude = ("finished_at",)

    @admin.display(description="Тема")
    def get_title(self, obj):
        return obj.message.get(obj.pk)

    @admin.display(description="Получатели")
    def get_receivers(self, obj):
        return [f"{receiver.full_name}: {receiver.email}" for receiver in obj.receivers.all()]


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("status", "get_receiver", "attempt_at")
    list_filter = ["attempt_at", "status"]
    search_fields = ("status",)
    exclude = ("mailing",)

    @admin.display(description="Получатель")
    def get_receiver(self, obj):
        return obj.server_answer.split()[-1] if obj.mailing.receivers.exists() else "Нет получателя"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
