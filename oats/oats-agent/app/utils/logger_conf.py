import logging
from logging.handlers import RotatingFileHandler
import datetime
import os


class AnsiColorFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': '\033[0;36m',
        'INFO': '\033[1;32m',
        'WARNING': '\033[1;33m',
        'ERROR': '\033[1;31m',
        'CRITICAL': '\033[1;41m'
    }

    def format(self, record):
        module_name = record.name.split('.')[-1]

        log_fmt = f'[%(asctime)s][%(levelname)s]({module_name}) %(message)s'
        if record.levelname in self.COLORS:
            levelname_color = self.COLORS[record.levelname]
            log_fmt = f"{levelname_color}{log_fmt}\033[0m"
            formatter = logging.Formatter(log_fmt)
            return formatter.format(record)
        else:
            return super().format(record)


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Directory for log files
    current_date = datetime.datetime.now().strftime("%Y%m%d")
    log_directory = os.path.join("logs", current_date)
    os.makedirs(log_directory, exist_ok=True)

    # Central log filename
    central_log_filename = 'central.log'
    central_file_handler = RotatingFileHandler(os.path.join(
        log_directory, central_log_filename), maxBytes=100000, backupCount=5)
    central_file_handler.setFormatter(AnsiColorFormatter())

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(AnsiColorFormatter())

    logger.addHandler(central_file_handler)
    logger.addHandler(console_handler)

    return logger
