import re
from functools import lru_cache

import sqlalchemy
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.orm import scoped_session, sessionmaker


class EnvVars(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="QUEUEBALL_", extra=None
    )

    db_uri: SecretStr
    connection_timeout: int = 2

    @property
    def engine(self) -> sqlalchemy.engine.Engine:
        return sqlalchemy.create_engine(
            self.db_uri.get_secret_value(),
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=5,
            connect_args={"connect_timeout": self.connection_timeout},
        )

    @property
    def session(self) -> scoped_session:
        default_kwargs = {"autocommit": False, "autoflush": False}
        kwargs = {**default_kwargs}
        return scoped_session(sessionmaker(**kwargs, bind=self.engine))

    @field_validator("db_uri", mode="before")
    def ensure_pymysql_uri(cls, v: str | SecretStr, __) -> SecretStr:
        if isinstance(v, SecretStr):
            v = v.get_secret_value()
        return SecretStr(re.sub("^mysql://", "mysql+pymysql://", v))


@lru_cache
def env_vars() -> EnvVars:
    return EnvVars()
