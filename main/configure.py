"""
Модуль, который предназначен для конфигурации объектов.
"""

import logging


def configure_logging():
    """
    Настраивает логинг в проекте.
    :return: logger.
    """
    logging.basicConfig(
        level=logging.DEBUG,
        filename="my_logging.log",
        format="%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]",
        datefmt="%d/%m/%Y %I:%M:%S",
        encoding="utf-8",
        filemode="w",
    )
    logger = logging.getLogger(__name__)
    handler = logging.FileHandler("my_logging.log", encoding="utf-8")
    formatter = logging.Formatter(
        "%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)
    return logger
