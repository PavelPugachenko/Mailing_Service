from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """This command sends emails to all receivers in the mailing.
        It takes the title of the message as an argument.
        You can also specify a list of recipient email addresses using the --recipients argument.
        To write a message text, use the --message argument.
        Example: python manage.py send_mail "Title of the message" --recipients user1@example.com user2@example.com
        --message your message"""

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Title of the message to send")
        parser.add_argument(
            "--recipients",
            nargs="+",
            type=str,
            help="List of recipient email addresses",
        )
        parser.add_argument(
            "--message",
            type=str,
            help="Text of the message to send",
        )

    def handle(self, *args, **kwargs):
        title = kwargs["title"]
        message = kwargs["message"]
        recipients = kwargs.get("recipients")
        self.__send_emails(title, message, recipients)

    def __send_emails(self, title, message, recipients=None):
        if recipients is None:
            self.stdout.write(self.style.ERROR("You didn't specify recipients email"))
        for receiver in recipients:
            try:
                send_mail(
                    subject=title,
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=False,
                )
            except BadHeaderError:
                return self.__handle_exception("Invalid header found.", receiver, title)
            except Exception as e:
                return self.__handle_exception(str(e), receiver, title)
            else:
                self.stdout.write(self.style.SUCCESS(f"Message '{title}' to '{receiver}' sent successfully"))

    def __handle_exception(self, error_message, receiver, title):
        self.stdout.write(self.style.ERROR(f"Message '{title}' sent to '{receiver}' failed: {error_message}"))
