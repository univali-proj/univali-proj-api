
from enum import StrEnum
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"

class BootstrapSettings(BaseSettings):
    APP_ENV: Environment = Environment.DEVELOPMENT

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

# Determina qual dotenv a classe Settings vai carregar
bootstrap = BootstrapSettings()

class Settings(BaseSettings):
    APP_NAME: str = "Confitto API"
    APP_ENV: Environment = bootstrap.APP_ENV
    DEBUG: bool = bootstrap.APP_ENV == Environment.DEVELOPMENT

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=(
            (".env", "local.env")
            if bootstrap.APP_ENV == "development"
            else ".env"
        ),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()  # pyright: ignore[reportCallIssue]


settings = get_settings()