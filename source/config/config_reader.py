from pydantic import PostgresDsn
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from redis.asyncio import Redis


class TelegramSettings(BaseSettings):
    bot_token: SecretStr
    admin_ids: list[int]
    webhook_use: bool
    webhook_path: str


class WebhookSettings(BaseSettings):
    url: str
    host: str
    port: int
    path: str
    secret: SecretStr


class DatabaseSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: SecretStr
    name: str

    def postgres_connection(self) -> str:
        return str(
            PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=self.user,
                password=self.password.get_secret_value(),
                host=self.host,
                port=self.port,
                path=self.name,
            ),
        )


class RedisSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: SecretStr
    db: int

    def redis_connection(self) -> Redis:
        return Redis(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password.get_secret_value(),
            db=self.db,
            decode_responses=True,
        )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )
    db: DatabaseSettings
    webhook: WebhookSettings
    tg: TelegramSettings
    redis: RedisSettings


settings = Settings()
