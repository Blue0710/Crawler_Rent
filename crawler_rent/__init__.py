import logging
from .logging_config import log_console, LogFileHandler

# Set logging file at the top package level
default_logger = logging.getLogger(__name__)
default_logger.setLevel(logging.INFO)
default_logger.addHandler(log_console)
default_logger.addHandler(LogFileHandler('./log/crawler_rent_log', logger_name=__name__))
