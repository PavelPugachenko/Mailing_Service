from django.db import models

from users.models import CustomUser


class MailReceiver(models.Model):
    email = models.EmailField(unique=True, verbose_name="Email")
    full_name = models.CharField(max_length=100)
    comment = models.TextField()
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="mailing_receivers", null=True, blank=True
    )

    def __str__(self):
        return f"{self.email}: {self.full_name}"

    class Meta:
        verbose_name = "Mail Receiver"
        verbose_name_plural = "Mail Receivers"
        ordering = ["email"]


class Message(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages", null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["title"]


class MailingUnit(models.Model):
    FINISHED = "Finished"
    CREATED = "Created"
    LAUNCHED = "Launched"

    STATUS_CHOICES = [(FINISHED, "Finished"), (CREATED, "Created"), (LAUNCHED, "Launched")]

    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Created")
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name="message")
    receivers = models.ManyToManyField(MailReceiver, related_name="mailing_units")
    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="mailing_units", null=True, blank=True
    )

    def __str__(self):
        return f"{self.message}: {self.status}"

    class Meta:
        verbose_name = "Mailing Unit"
        verbose_name_plural = "Mailing Units"
        ordering = ["-status", "started_at"]
        permissions = [("can_disable_mailing", "Can disable mailing")]


class MailingAttempt(models.Model):
    SUCCESS = "Success"
    FAILED = "Failed"

    STATUS_CHOICES = [(SUCCESS, "Success"), (FAILED, "Failed")]

    attempt_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    server_answer = models.TextField()
    mailing = models.ForeignKey(MailingUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mailing}: {self.status} ({self.attempt_at})"

    class Meta:
        verbose_name = "Mailing Attempt"
        verbose_name_plural = "Mailing Attempts"
        ordering = [
            "-attempt_at",
            "mailing",
            "status",
        ]
        permissions = [("can_view_report", "Can view report")]
