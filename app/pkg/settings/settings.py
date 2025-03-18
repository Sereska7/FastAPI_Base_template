"""Module for load settings form `.env` or if server running with parameter
`dev` from `.env.dev`"""

import urllib.parse
from functools import cached_property, lru_cache

import jwt
from dotenv import find_dotenv
from pydantic import (
    AmqpDsn,
    ClickHouseDsn,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    computed_field,
    model_validator,
)
from pydantic.types import PositiveInt, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.pkg.models.base.settings_enum import EnvironmentEnum
from app.pkg.models.core.logger import LoggerLevel

__all__ = ["Settings", "get_settings"]


class _Settings(BaseSettings):
    """Base settings for all settings.

    Use double underscore for nested env variables.

    Examples:
        `.env` file should look like::

            TELEGRAM__TOKEN=...
            TELEGRAM__WEBHOOK_DOMAIN_URL=...

            LOGGER__PATH_TO_LOG="./src/logs"
            LOGGER__LEVEL="DEBUG"

            API_SERVER__HOST="127.0.0.1"
            API_SERVER__PORT=9191

    Warnings:
        In the case where a value is specified for the same Settings field in multiple
        ways, the selected value is determined as follows
        (in descending order of priority):

        1. Arguments passed to the Settings class initializer.
        2. Environment variables, e.g., my_prefix_special_function as described above.
        3. Variables loaded from a dotenv (.env) file.
        4. Variables loaded from the secrets directory.
        5. The default field values for the Settings model.

    See Also:
        https://docs.pydantic.dev/latest/usage/pydantic_settings/
    """

    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        arbitrary_types_allowed=True,
        case_sensitive=True,
        env_nested_delimiter="__",
        coerce_numbers_to_str=True,
        extra="ignore",
    )


class Postgresql(_Settings):
    """Postgresql settings."""

    #: str: Postgresql host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of postgresql.
    PORT: PositiveInt = 5432
    #: str: Postgresql user.
    USER: str = "postgres"
    #: SecretStr: Postgresql password.
    PASSWORD: SecretStr = SecretStr("postgres")
    #: str: Postgresql database name.
    DATABASE_NAME: str = "postgres"

    #: PositiveInt: Min count of connections in one pool to postgresql.
    MIN_CONNECTION: PositiveInt = 1
    #: PositiveInt: Max count of connections in one pool  to postgresql.
    MAX_CONNECTION: PositiveInt = 16

    #: str: Concatenation all settings for postgresql in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: str | None = None

    TEST_DSN: str | None = None

    @model_validator(mode="before")
    @classmethod
    def build_dsn(cls, data: dict) -> dict:
        """Build DSN for postgresql.

        Args:
            data: dict with all settings.

        Notes:
            This method is called before any other validation.
            I use it to build DSN for postgresql.

        See Also:
            About validators:
                https://docs.pydantic.dev/latest/concepts/validators/#model-validators

            About DSN:
                https://pydantic-docs.helpmanual.io/usage/types/#postgresdsn

        Returns:
            dict with all settings and DSN.
        """

        data["DSN"] = str(
            PostgresDsn.build(
                scheme="postgresql",
                username=data.get("USER"),
                password=urllib.parse.quote_plus(data.get("PASSWORD")),
                host=data.get("HOST"),
                port=int(data.get("PORT")),
                path=data.get("DATABASE_NAME"),
            ),
        )

        data["TEST_DSN"] = str(
            PostgresDsn.build(
                scheme="postgresql",
                username=data.get("USER"),
                password=urllib.parse.quote_plus(data.get("PASSWORD")),
                host=data.get("HOST"),
                port=int(data.get("PORT")),
                path=f"test_{data.get("DATABASE_NAME")}",
            ),
        )
        return data


class Clickhouse(_Settings):
    """Clickhouse settings."""

    HOST: str = "localhost"
    PORT: PositiveInt = 8123
    PASSWORD: SecretStr = SecretStr("password")
    USER: str = "default"
    DB: str = "default"
    DSN: str | None = None

    @model_validator(mode="before")
    @classmethod
    def build_click_dsn(cls, data: dict) -> dict:
        """Build DSN for postgresql.

        Args:
            data: dict with all settings.

        Notes:
            This method is called before any other validation.
            I use it to build DSN for redis.

        Returns:
            dict with all settings and DSN.
        """

        data["DSN"] = str(
            ClickHouseDsn.build(
                scheme="clickhouse",
                username=data["USER"],
                password=urllib.parse.quote_plus(data["PASSWORD"]),
                host=data["HOST"],
                port=int(data["PORT"]),
                path=data["DB"],
            ),
        )
        return data


class RabbitMQ(_Settings):
    """RabbitMQ settings."""

    #: str: Resource host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of Resource.
    PORT: PositiveInt = 5672
    #: str: Resource user.
    USER: str = "user"
    #: SecretStr: Resource password.
    PASSWORD: SecretStr = "secret"
    #: Connection DSN schema
    SCHEMA: str = "amqp"

    BID_QUEUE_NAME: str
    BID_QUEUE_NAME_SECOND: str

    #: str: Concatenation all settings for Resource in one string. (DSN)
    #  Builds in `root_validator` method.
    DSN: str | None = None

    @model_validator(mode="before")
    @classmethod
    def build_dsn(cls, values: dict) -> dict:  # noqa: A003
        values["DSN"] = str(
            AmqpDsn.build(
                scheme="amqp",
                username=values["USER"],
                password=urllib.parse.quote_plus(values["PASSWORD"]),
                host=values["HOST"],
                port=int(values["PORT"]),
            ),
        )
        return values


class Redis(_Settings):
    """Redis settings."""

    HOST: str = "localhost"
    PORT: PositiveInt = 6379
    PASSWORD: SecretStr = SecretStr("password")
    DB: int = 0
    DSN: str | None = None

    @model_validator(mode="before")
    @classmethod
    def build_dsn(cls, values: dict) -> dict:
        """Build DSN for postgresql.

        Args:
            values: dict with all settings.

        Notes:
            This method is called before any other validation.
            I use it to build DSN for redis.

        Returns:
            dict with all settings and DSN.
        """

        values["DSN"] = str(
            RedisDsn.build(
                scheme="redis",
                password=urllib.parse.quote_plus(values["PASSWORD"]),
                host=values["HOST"],
                port=int(values["PORT"]),
                path=values["DB"],
            ),
        )
        return values


class Logging(_Settings):
    """Logging settings."""

    #: StrictStr: Level of logging which outs in std
    LEVEL: LoggerLevel = LoggerLevel.DEBUG


class APIServer(_Settings):
    """API settings."""

    # --- API SETTINGS ---
    #: str: API host.
    HOST: str = "localhost"

    # --- SECURITY SETTINGS ---
    #: SecretStr: Secret key for token auth.
    X_API_TOKEN: SecretStr = SecretStr("secret")

    # --- OTHER SETTINGS ---
    #: Logging: Logging settings.
    LOGGER: Logging

    DEBUG_MODE: bool = False

    # Now used only for logging level
    ENVIROMENT: EnvironmentEnum = EnvironmentEnum.DEV.value


class Centrifugo(_Settings):
    """Centrifugo settings."""

    #: str: Centrifugo host.
    HOST: str = "localhost"
    #: PositiveInt: positive int (x > 0) port of centrifugo.
    PORT: PositiveInt = 8001
    #: SecretStr: encryption token for jwt authentication in centrifugo.
    TOKEN_HMAC_SECRET_KEY: SecretStr = SecretStr("TOKEN_HMAC_SECRET_KEY")
    #: SecretStr: token for getting access to centrifugo HTTP API.
    X_API_KEY: SecretStr = SecretStr("API_KEY")
    #: str: Centrifugo websocket path,
    WEBSOCKET_PATH: str = "/connection/uni_websocket"
    USER_ID: str = "1"
    CHANNEL_COUNTRY_CREATE: str = "country:create"
    CHANNEL_CITY_CREATE: str = "city:create"

    @computed_field
    @cached_property
    def CHANNELS(self) -> tuple[str, ...]:
        """Build CHANNELS tuple.

        Returns:
            tuple[str, ...]: centrifugo channels.
        """
        return tuple(
            value
            for field, value in self.__dict__.items()
            if field.startswith("CHANNEL_")
        )

    @computed_field
    @cached_property
    def URL(self) -> str:
        """Build URL for centrifugo.

        Notes:
            This method is called once.
            I use it to build URL for centrifugo.

        Returns:
            str: centrifugo URL.
        """
        return str(
            HttpUrl.build(
                scheme="http",
                host=self.HOST,
                port=int(self.PORT),
            ),
        )

    @computed_field
    @cached_property
    def WS_URL(self) -> str:
        """Build websocket URL for centrifugo.

        Notes:
            This method is called once.
            I use it to build websocket URL for centrifugo.

        Returns:
            str: centrifugo websocket URL.
        """

        return str(
            HttpUrl.build(
                scheme="ws",
                host=self.HOST,
                port=int(self.PORT),
                path=self.WEBSOCKET_PATH,
            ),
        )

    @computed_field
    @cached_property
    def JWT_TOKEN(self) -> str:
        """Build JWT for centrifugo.

        Notes:
            This method is called once.
            I use it to build JWT for centrifugo.

        Returns:
            str: jwt with encoded user information.
        """
        return jwt.encode(
            {"sub": self.USER_ID}, self.TOKEN_HMAC_SECRET_KEY.get_secret_value(),
        )


class Clients(_Settings):
    """Clients settings."""

    #: Centrifugo
    CENTRIFUGO: Centrifugo


class Settings(_Settings):
    """Server settings.

    Formed from `.env` or `.env.dev` if server running with parameter
    `dev`.
    """

    #: APIServer: API settings. Contains all settings for API.
    API: APIServer

    #: Postgresql: Postgresql settings.
    POSTGRES: Postgresql

    #: Clickhouse: Clickhouse settings.
    CLICKHOUSE: Clickhouse

    #: Rabbit
    RABBITMQ: RabbitMQ

    #: Redis
    REDIS: Redis

    #: Clients
    CLIENTS: Clients

@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""

    return Settings(_env_file=find_dotenv(env_file))
