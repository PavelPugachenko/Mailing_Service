import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from mailing.models import MailingAttempt, MailingUnit

logger = logging.getLogger(__name__)


def send_emails():
    mailing_units = MailingUnit.objects.filter(status="Launched")
    for mailing_unit in mailing_units:
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
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Success", server_answer=f"Email успешно отправлен для {receiver}"
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing_unit,
                    status="Failed",
                    server_answer=f'Возникла ошибка: "{str(e)}" при отправке на {receiver}',
                )
        mailing_unit.status = "Launched"
        mailing_unit.save()


@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_emails,
            trigger=CronTrigger(hour="14", minute="30"),
            id="send_emails",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_emails' to run at 11:30 AM every day.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour="15", minute="00"),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
