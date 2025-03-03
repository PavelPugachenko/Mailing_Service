from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from users.services import CustomUserService

from .forms import MailingUnitForm, MailReceiverForm, MessageForm
from .logger import mail_logger
from .models import MailingAttempt, MailingUnit, MailReceiver, Message
from .services import CACHE_TIMEOUT, MailingAttemptService, MailingUnitService, MailReceiverService, MessageService


class MailingView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm("mailing.view_mailingunit"):
            all_mailings = MailingUnitService.get_all_mailing_units(count=True)
            launched_mailings = MailingUnitService.get_all_launched_mailing_units(count=True)
            unique_receivers = MailReceiverService.get_all_mail_receivers(count=True)
            mail_logger.info(
                f"""Counted all mailings, launched mailings and unique
            receivers for manager {self.request.user}"""
            )
        else:
            all_mailings = MailingUnitService.get_owner_mailing_units(request.user.id, count=True)
            launched_mailings = MailingUnitService.get_owner_launched_mailing_units(request.user.id, count=True)
            unique_receivers = MailReceiverService.get_owner_mail_receivers(request.user.id, count=True)
            mail_logger.info(
                f"""Counted user-specific mailings, launched mailings
            and unique receivers for user {self.request.user}"""
            )

        context = {
            "all_mailings": all_mailings,
            "launched_mailings": launched_mailings,
            "unique_receivers": unique_receivers,
        }

        return render(request, "mailing/home.html", context)


class MailReceiverListView(LoginRequiredMixin, ListView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receivers_list.html"
    context_object_name = "mail_receivers"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_mailreceiver"):
            mail_logger.info(f"Manager {self.request.user} is viewing all mail receivers")
            return MailReceiverService.get_all_mail_receivers()
        mail_logger.info(f"User {self.request.user} is viewing their mail receivers")
        return MailReceiverService.get_owner_mail_receivers(self.request.user.id)


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class MailReceiverDetailView(LoginRequiredMixin, DetailView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receiver_detail.html"
    context_object_name = "mail_receiver"


class MailReceiverCreateView(LoginRequiredMixin, CreateView):
    model = MailReceiver
    form_class = MailReceiverForm
    template_name = "mailing/mail_receiver/mail_receiver_form.html"
    context_object_name = "mail_receiver"
    success_url = reverse_lazy("mailing:mail-receivers-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mail_logger.info(f"User {self.request.user} created a new mail receiver {form.instance}")
        return super().form_valid(form)


class MailReceiverUpdateView(LoginRequiredMixin, UpdateView):
    model = MailReceiver
    form_class = MailReceiverForm
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_form.html"

    def get_success_url(self):
        messages.success(
            self.request,
            f"Mail receiver updated successfully. Changes will be displayed after {CACHE_TIMEOUT} seconds",
        )
        return reverse_lazy("mailing:mail-receivers-list")


class MailReceiverDeleteView(LoginRequiredMixin, DeleteView):
    model = MailReceiver
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_delete.html"
    success_url = reverse_lazy("mailing:home")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message/messages_list.html"
    context_object_name = "all_messages"

    def get_queryset(self):
        mail_logger.info(f"User {self.request.user} is viewing their messages")
        return MessageService.get_owner_messages(self.request.user.id)


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message/message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mail_logger.info(f"User {self.request.user} created a new message")
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"

    def get_success_url(self):
        messages.success(
            self.request,
            f"Message updated successfully. Changes inside message will be displayed after {CACHE_TIMEOUT} seconds",
        )
        return reverse_lazy("mailing:messages-list")


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    context_object_name = "message"
    template_name = "mailing/message/message_delete.html"
    success_url = reverse_lazy("mailing:home")


class MailingUnitListView(LoginRequiredMixin, ListView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_units_list.html"
    context_object_name = "mailing_units"

    def get_queryset(self):
        if self.request.user.has_perm("mailing.view_mailingunit"):
            mail_logger.info(f"Manager {self.request.user} is viewing all mailing units")
            return MailingUnitService.get_all_mailing_units()
        mail_logger.info(f"User {self.request.user} is viewing their mailing units")
        return MailingUnitService.get_owner_mailing_units(self.request.user.id)


@method_decorator(cache_page(CACHE_TIMEOUT), name="dispatch")
class MailingUnitDetailView(LoginRequiredMixin, DetailView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"
    context_object_name = "mailing_unit"


class MailingUnitCreateView(LoginRequiredMixin, CreateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"
    success_url = reverse_lazy("mailing:mailing-units-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        mail_logger.info(f"User {self.request.user} created a new mailing unit")
        return super().form_valid(form)


class MailingUnitUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"

    def get_success_url(self):
        messages.success(
            self.request, f"Mailing updated successfully. Changes will be displayed after {CACHE_TIMEOUT} seconds"
        )
        return reverse_lazy("mailing:mailing-units-list")


class MailingUnitDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_delete.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitSendMailView(LoginRequiredMixin, View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        self.send_emails(mailing_unit)
        self.update_status(mailing_unit, "Launched")
        mail_logger.info(f"User {self.request.user} sent emails for mailing unit {mailing_unit.message}")
        return redirect("mailing:mailing-units-list")

    def send_emails(self, mailing_unit):
        recipients = [receiver.email for receiver in mailing_unit.receivers.all()]
        for receiver in recipients:
            try:
                send_mail(
                    subject=mailing_unit.message.title,
                    message=mailing_unit.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=False,
                )
            except BadHeaderError:
                return self.handle_exception("Invalid header found.", receiver, mailing_unit)
            except Exception as e:
                return self.handle_exception(str(e), receiver, mailing_unit)
            else:
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Success", server_answer=f"Email sent to {receiver}"
                )

    def handle_exception(self, error_message, receiver, mailing_unit):
        MailingAttempt.objects.create(
            mailing=mailing_unit,
            status="Failed",
            server_answer=f'Error occured: "{error_message}" when sending to {receiver}',
        )
        return HttpResponse(error_message)

    def update_status(self, mailing_unit, status):
        if mailing_unit.status != status:
            mailing_unit.status = status
            mailing_unit.save()


class MailingUnitStopMailView(LoginRequiredMixin, View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        mailing_unit.status = "Finished"
        mailing_unit.finished_at = timezone.now()
        mailing_unit.save()
        mail_logger.info(f"User {self.request.user} stopped mailing unit {mailing_unit}")
        return redirect("mailing:mailing-units-list")


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/mailing_attempts_list.html"
    context_object_name = "mailing_attempts"
    ordering = ["-attempt_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_queryset().exists():
            context["message"] = self.get_queryset().first().mailing.message
        return context

    def get_queryset(self):
        mailing_id = self.kwargs.get("mailing_id")
        if mailing_id:
            return MailingAttemptService.get_mailing_attempts_by_mailing(mailing_id).order_by("-attempt_at")
        return MailingAttemptService.get_mailing_attempts_by_owner(self.request.user).order_by("-attempt_at")


class ReportView(LoginRequiredMixin, PermissionRequiredMixin, View):

    permission_required = "mailing.can_view_report"

    def get(self, request):
        users = CustomUserService.get_all_users()
        user_attempts = []

        for user in users:
            total_attempts = MailingAttemptService.get_mailing_attempts_by_owner(user, count=True)
            successful_attempts = MailingAttemptService.get_mailing_attempts_by_status(
                owner=user, status="Success", count=True
            )
            failed_attempts = MailingAttemptService.get_mailing_attempts_by_status(
                owner=user, status="Failed", count=True
            )
            user_attempts.append(
                {
                    "user": user,
                    "total_attempts": total_attempts,
                    "successful_attempts": successful_attempts,
                    "failed_attempts": failed_attempts,
                }
            )

        context = {
            "user_attempts": user_attempts,
        }
        mail_logger.info(f"Manager {self.request.user} is viewing the report")
        return render(request, "mailing/reports.html", context)
