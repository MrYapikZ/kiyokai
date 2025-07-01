from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    APP_PORT: int = 8741

    DATABASE_URL: str = os.environ.get("DATABASE_URL")

    # Add cookie config
    COOKIE_REFRESH_TOKEN_NAME: str = "refresh_token"
    COOKIE_SECURE: bool = False
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    COOKIE_MAX_AGE: int = 60 * 60 * 24 * 7  # 7 days

    class Config:
        env_file = ".env"
        frozen = False  # Allow settings to be modified after initialization

settings = Settings()