import logging

from config import settings

LOG_LEVEL = logging.DEBUG

formatter = settings.formatter

handler = logging.StreamHandler()
handler.setFormatter(formatter)

users_logger = logging.getLogger()
users_logger.setLevel(LOG_LEVEL)
users_logger.addHandler(handler)
