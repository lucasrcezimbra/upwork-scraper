import logging

from upwork import settings


def get_logger(name):
    formatter = logging.Formatter(
        '%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)

    return logger
