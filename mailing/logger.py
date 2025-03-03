import logging

from config import settings

LOG_LEVEL = logging.DEBUG

formatter = settings.formatter

handler = logging.StreamHandler()
handler.setFormatter(formatter)

mail_logger = logging.getLogger()
mail_logger.setLevel(LOG_LEVEL)
mail_logger.addHandler(handler)
