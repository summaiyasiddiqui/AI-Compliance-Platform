from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import validator


class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    frontend_url: str = "http://localhost:5173"

    database_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    resend_api_key: str
    email_from: str

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @validator("debug")
    def validate_debug(cls, value, values):
        if values.get("environment", "").lower() == "production" and value:
            raise ValueError("DEBUG must be False in production.")
        return value


settings = Settings()