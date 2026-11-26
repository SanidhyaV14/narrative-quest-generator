import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./narrative_studio.db"

    # JWT Authentication
    JWT_SECRET_KEY: str = "narrative_studio_dev_secret_key_change_in_production_2026_x99"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # NVIDIA AI Service
    NVIDIA_API_KEY: str = ""
    NEMOTRON_MODEL: str = "nvidia/nemotron-3.5-super-vl-120b-a12b"
    NEMOTRON_VL_MODEL: str = "nvidia/nemotron-3.5-super-vl-120b-a12b"
    NEMOTRON_BASE_URL: str = "https://integrate.api.nvidia.com/v1"

    FLUX_MODEL: str = "black-forest-labs/flux.1-dev"
    FLUX_BASE_URL: str = "https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev"

    # Uploads & Storage
    MAX_UPLOAD_SIZE_MB: int = 5
    UPLOAD_REFERENCES_DIR: str = "uploads/references"
    UPLOAD_GENERATED_DIR: str = "uploads/generated"

    # Server Ports
    BACKEND_HOST: str = "127.0.0.1"
    BACKEND_PORT: int = 8000
    API_BASE_URL: str = "http://127.0.0.1:8000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

# Ensure upload directories exist
os.makedirs(settings.UPLOAD_REFERENCES_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_GENERATED_DIR, exist_ok=True)
