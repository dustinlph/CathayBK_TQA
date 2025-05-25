import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timezone, timedelta
import os


def setup_logger(module_name: str):
    LOG_DIR = os.path.join(os.getcwd(), "logs")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    LOG_FILE = os.path.join(
        LOG_DIR,
        f"{datetime.now(timezone(timedelta(hours=8))).strftime('%Y%m%d_%H%M%S')}.log"
    )

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - [%(thread)d]%(threadName)s - %(message)s')

    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
