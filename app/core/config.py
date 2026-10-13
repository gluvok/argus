"""Runtime environment configuration for Argus ANPR."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime environment configuration loaded from .env or environment variables."""

    ENABLE_MULTI_VEHICLE_OCR: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
