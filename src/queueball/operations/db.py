import logging
import contextlib

from sqlalchemy.exc import OperationalError

from queueball.config import env_vars
from queueball.db import Base

logger = logging.getLogger(__name__)


def create_tables():
    """Create tables using the SQLAlchemy table registry"""
    logger.info("Starting table creation")

    with env_vars().session() as session:
        Base.metadata.create_all(bind=session.get_bind())

    logger.info("Tables created successfully.")


def drop_tables():
    """Drop tables defined using the SQLAlchemy table registry"""
    logger.info("Starting table deletion")

    with env_vars().session() as session:
        for table in reversed(Base.metadata.sorted_tables):
            with contextlib.suppress(OperationalError):
                table.drop(bind=session.get_bind())

    logger.info("Tables dropped successfully")
