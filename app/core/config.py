from enum import StrEnum
from functools import lru_cache
from pathlib import Path
import os

from dotenv import dotenv_values
from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[2]
BASE_ENV_FILE = BASE_DIR / ".env"
LOCAL_ENV_FILE = BASE_DIR / "local.env"


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TESTING = "testing"


def load_environment() -> Environment:
    """Resolve o APP_ENV com prioridade: variável do SO > local.env (apenas em desenvolvimento) > .env > development."""
    if value := os.getenv("APP_ENV"):
        return Environment(value.lower())

    value = dotenv_values(BASE_ENV_FILE).get("APP_ENV") or Environment.DEVELOPMENT
    environment = Environment(value.lower())

    if environment == Environment.DEVELOPMENT:
        local_value = dotenv_values(LOCAL_ENV_FILE).get("APP_ENV")
        if local_value:
            environment = Environment(local_value.lower())

    return environment


def get_env_files(environment: Environment) -> tuple[Path, ...]:
    # O pydantic-settings dá prioridade ao último arquivo da tupla
    if environment == Environment.DEVELOPMENT:
        return (BASE_ENV_FILE, LOCAL_ENV_FILE)
    return (BASE_ENV_FILE,)


class Settings(BaseSettings):
    APP_NAME: str = "Confitto API"
    APP_VERSION: str = "0.1.0"
    APP_ENV: Environment = Environment.DEVELOPMENT
    DEBUG: bool | None = None

    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = []

    LOG_LEVEL: str = "INFO"

    DATABASE_URL: str
    SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    @model_validator(mode="after")
    def _default_debug(self) -> "Settings":
        if self.DEBUG is None:
            self.DEBUG = self.APP_ENV == Environment.DEVELOPMENT
        return self

    @property
    def is_development(self) -> bool:
        return self.APP_ENV == Environment.DEVELOPMENT

    @property
    def is_production(self) -> bool:
        return self.APP_ENV == Environment.PRODUCTION


@lru_cache
def get_settings(environment: Environment | None = None) -> Settings:
    environment = environment or load_environment()
    return Settings(  
        _env_file=get_env_files(environment), # pyright: ignore[reportCallIssue]
        APP_ENV=environment,
    )
