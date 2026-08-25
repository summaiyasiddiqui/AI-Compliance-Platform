from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    environment: str = "development"
    debug: bool = False
    frontend_url: str = "http://localhost:5173"
    allowed_hosts: str = "localhost,127.0.0.1"

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

@field_validator("debug")
@classmethod
def validate_debug(cls, value, info):
    if info.data.get("environment", "").lower() == "production" and value:
        raise ValueError("DEBUG must be False in production.")
    return value

settings = Settings()
