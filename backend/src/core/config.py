import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from envparse import Env
from pydantic import (
    BaseModel,
    Field,
    PostgresDsn,
    ValidationInfo,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_FOLDER = Path(__file__).parent.parent.parent


class PostgresSettings(BaseModel):
    driver: str
    host: str
    port: int
    user: str
    password: str
    db: str

    uri: Optional[PostgresDsn] = Field(None, validate_default=True)

    @field_validator("uri", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme=f"postgresql+{values.data.get('driver')}",
            username=values.data.get("user"),
            password=values.data.get("password"),
            host=f"{values.data.get('host')}:{values.data.get('port')}",
            path=f"{values.data.get('db') or ''}",
        )


class CoreSettings(BaseSettings):
    project_folder: Path = PROJECT_FOLDER
    project_name: str
    secret_key: str = secrets.token_urlsafe(32)
    debug: bool = False


class Settings(BaseSettings):
    core: CoreSettings = Field(default_factory=CoreSettings)
    postgres: PostgresSettings

    model_config = SettingsConfigDict(env_nested_delimiter="_")


@lru_cache
def get_settings() -> Settings:
    env = Env()
    env.read_envfile()

    return Settings()
