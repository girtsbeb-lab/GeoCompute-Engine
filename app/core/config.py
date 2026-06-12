from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "GeoCompute Engine"
    app_env: str = "development"
    database_url: str = "postgresql+psycopg2://geocompute:geocompute@localhost:5432/geocompute"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
