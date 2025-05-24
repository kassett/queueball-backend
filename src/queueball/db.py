from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer, MetaData, String, func, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base is a SQLAlchemy requirement that unifies all tables into a registry

    We also use base to ensure that all tables have
        * standard patterns for indexes and constraints
        * a created timestamp
        * an updated timestamp
    """

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    created: Mapped[datetime] = mapped_column(
        TIMESTAMP(), nullable=False, server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        TIMESTAMP(),
        nullable=False,
        server_default=text("NOW() ON UPDATE NOW()"),
    )


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(100), primary_key=True, nullable=False)
    email: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    profile_picture: Mapped[str | None] = mapped_column(String(255), nullable=True)


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[str] = mapped_column(
        Integer(), primary_key=True, nullable=False, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    address: Mapped[str | None] = mapped_column(String(255), nullable=True)
    instagram_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    google_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    qr_code_url: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # Will be an S3 URL
