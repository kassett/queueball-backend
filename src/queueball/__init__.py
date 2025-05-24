import logging
from logging import Logger

from pydantic_settings import BaseSettings, SettingsConfigDict


VERSION = "0.1.0"

class LogLevel(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra=None)

    log_level: str = "INFO"


def getLogger(name: str = "queueball") -> Logger:
    logger = logging.getLogger(name)

    # only add a handler if this logger has none yet
    if not logger.handlers:
        ch = logging.StreamHandler()
        fmt = logging.Formatter(
            "%(asctime)s %(levelname)-8s %(name)s: %(message)s"
        )
        ch.setFormatter(fmt)
        logger.addHandler(ch)

    # look up the desired level (default INFO)
    level_name = LogLevel().log_level.upper()
    level = getattr(logging, level_name, logging.INFO)
    logger.setLevel(level)

    return logger
