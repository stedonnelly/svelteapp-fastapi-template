from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    ENV: str = "development"
    PROJECT_NAME: str = "My App"
    SECRET_KEY: str = "change_me"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "app_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # CORS / Frontend origin(s)
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173", "http://localhost"]
    SECURE_COOKIES: bool = False  # set True in prod

    SESSION_COOKIE_NAME: str = "sessionid"
    SESSION_MAX_AGE_SECONDS: int = 60 * 60 * 24 * 7  # 7 days

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @field_validator("ALLOWED_ORIGINS", mode="before")
    @classmethod
    def split_origins(cls, v):
        if isinstance(v, str):
            # allow comma-separated in .env
            return [s.strip() for s in v.split(",") if s.strip()]
        return v


settings = Settings()
