from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/crm_db"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    secret_key: str = "your-secret-key-change-in-production"
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
