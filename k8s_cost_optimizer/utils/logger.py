import logging


LOGGER_NAME = "k8s-cost-optimizer"


def get_logger():

    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
