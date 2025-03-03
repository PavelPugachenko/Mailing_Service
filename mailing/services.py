from django.core.cache import cache

from config.settings import CACHE_ENABLED

from .models import MailingAttempt, MailingUnit, MailReceiver, Message

CACHE_TIMEOUT = 60


def count_total(queryset, count):
    """Return the total count of the queryset if count is True, otherwise return the queryset itself."""
    return queryset.count() if count else queryset


def get_queryset_or_count(query, key, count, **query_options):
    queryset = cache.get(key)
    if queryset is not None:
        return count_total(queryset, count)
    queryset = query(**query_options)
    cache.set(key, queryset, CACHE_TIMEOUT)
    return count_total(queryset, count)


class MailingUnitService:

    @staticmethod
    def get_all_mailing_units(count=False):
        """Return all mailing units if count is False otherwise return total amount of queried mailing units."""
        mailing_units = MailingUnit.objects.all
        if not CACHE_ENABLED:
            return count_total(mailing_units(), count)
        key = "mailing_units"
        return get_queryset_or_count(mailing_units, key, count)

    @staticmethod
    def get_owner_mailing_units(owner_id, count=False):
        """Return all mailing units of the owner if count is False
        otherwise return total amount of queried mailing units."""
        mailing_units = MailingUnit.objects.filter
        if not CACHE_ENABLED:
            return count_total(mailing_units(owner_id=owner_id), count)
        key = f"owner_mailing_units_{owner_id}"
        return get_queryset_or_count(mailing_units, key, count, owner_id=owner_id)

    @staticmethod
    def get_all_launched_mailing_units(count=False):
        """Return all launched mailing units if count is False
        otherwise return total amount of queried mailing units."""
        mailing_units = MailingUnit.objects.filter
        if not CACHE_ENABLED:
            return count_total(mailing_units(status="Launched"), count)
        key = "launched_mailing_units"
        return get_queryset_or_count(mailing_units, key, count, status="Launched")

    @staticmethod
    def get_owner_launched_mailing_units(owner_id, count=False):
        """Return all launched mailing units of the owner if count is False
        otherwise return total amount of queried mailing units."""
        mailing_units = MailingUnit.objects.filter
        if not CACHE_ENABLED:
            return count_total(mailing_units(owner_id=owner_id, status="Launched"), count)
        key = f"owner_launched_mailing_units_{owner_id}"
        return get_queryset_or_count(mailing_units, key, count, owner_id=owner_id, status="Launched")


class MessageService:

    @staticmethod
    def get_owner_messages(owner_id):
        """Return all messages of the owner."""
        if not CACHE_ENABLED:
            return Message.objects.filter(owner_id=owner_id)
        key = f"owner_messages_{owner_id}"
        messages = cache.get(key)
        if messages is not None:
            return messages
        messages = Message.objects.filter(owner_id=owner_id)
        cache.set(key, messages, CACHE_TIMEOUT)
        return messages


class MailReceiverService:

    @staticmethod
    def get_all_mail_receivers(count=False):
        """Return all mail receivers if count is False
        otherwise return total amount of queried mail receivers."""
        mail_receivers = MailReceiver.objects.all
        if not CACHE_ENABLED:
            return count_total(mail_receivers(), count)
        key = "mail_receivers"
        return get_queryset_or_count(mail_receivers, key, count)

    @staticmethod
    def get_owner_mail_receivers(owner_id, count=False):
        """Return all mail receivers of the owner if count is False
        otherwise return total amount of queried mail receivers."""
        mail_receivers = MailReceiver.objects.filter
        if not CACHE_ENABLED:

            return count_total(mail_receivers(owner_id=owner_id), count)
        key = f"owner_mail_receivers_{owner_id}"
        return get_queryset_or_count(mail_receivers, key, count, owner_id=owner_id)


class MailingAttemptService:

    @staticmethod
    def get_mailing_attempts_by_mailing(mailing_id, count=False):
        """Return all mailing attempts of the mailing if count is False
        otherwise return total amount of queried mailing attempts."""
        mailing_attempts = MailingAttempt.objects.filter
        if not CACHE_ENABLED:

            return count_total(mailing_attempts(mailing=mailing_id), count)
        key = f"mailing_attempts_{mailing_id}"
        return get_queryset_or_count(mailing_attempts, key, count, mailing=mailing_id)

    @staticmethod
    def get_mailing_attempts_by_owner(owner, count=False):
        """Return all mailing attempts of the owner if count is False
        otherwise return total amount of queried mailing attempts."""
        mailing_attempts = MailingAttempt.objects.filter
        if not CACHE_ENABLED:

            return count_total(mailing_attempts(mailing__owner=owner), count)
        key = f"mailing_attempts_{owner}"
        return get_queryset_or_count(mailing_attempts, key, count, mailing__owner=owner)

    @staticmethod
    def get_mailing_attempts_by_status(owner, status, count=False):
        """Return all mailing attempts of the owner with the specified status if count is False
        otherwise return total amount of queried mailing attempts."""
        mailing_attempts = MailingAttempt.objects.filter
        if not CACHE_ENABLED:

            return count_total(mailing_attempts(status=status, mailing__owner=owner), count)
        key = f"mailing_attempts_{owner}_{status}"
        return get_queryset_or_count(mailing_attempts, key, count, status=status, mailing__owner=owner)
