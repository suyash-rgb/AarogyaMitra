# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Core Application Settings
    APP_NAME: str = "ArogyaMitra API Backend"
    ENVIRONMENT: str = "development"
    
    # Database Settings
    DATABASE_URL: Optional[str] = None
    
    # Ola Maps API Settings
    OLA_MAPS_KRUTRIM_CLOUD_API_KEY: Optional[str] = None
    OLA_MAPS_KRUTRIM_CLOUD_API_BASE_URL: str = "https://api.olamaps.io"

    # Valkey Cache Settings
    VALKEY_HOST: str = "localhost"
    VALKEY_PORT: int = 6379
    VALKEY_DB: int = 0
    VALKEY_TTS_TTL_SECONDS: int = 86400
    VALKEY_TRANS_TTL_SECONDS: int = 604800
    VALKEY_GEO_TTL_SECONDS: int = 7200
    VALKEY_RAG_TTL_SECONDS: int = 86400
    VALKEY_INTENT_TTL_SECONDS: int = 604800

    @property
    def resolved_ola_maps_api_key(self) -> str:
        return self.OLA_MAPS_KRUTRIM_CLOUD_API_KEY or ""

    @property
    def resolved_ola_maps_base_url(self) -> str:
        return self.OLA_MAPS_KRUTRIM_CLOUD_API_BASE_URL or "https://api.olamaps.io"

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

settings = Settings()
