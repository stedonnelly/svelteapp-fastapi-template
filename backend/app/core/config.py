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
        # accept None / empty -> []
        if v is None:
            return []
        # already a list -> return as-is
        if isinstance(v, (list | tuple)):
            return list(v)
        # handle empty string
        if isinstance(v, str):
            s = v.strip()
            if not s:
                return []
            # allow JSON-style list: ["a","b"] or ['a','b']
            if s.startswith("[") and s.endswith("]"):
                try:
                    import json

                    parsed = json.loads(s)
                    if isinstance(parsed, list):
                        return parsed
                except Exception:
                    # fall through to comma-splitting
                    print(
                        "WARNING: ALLOWED_ORIGINS looks like a JSON list but could not be parsed"
                        ", falling back to comma-splitting"
                    )
            # comma-separated values
            return [p.strip() for p in s.split(",") if p.strip()]
        # fallback: let pydantic handle/validate the value and fail loudly if invalid
        return v


settings = Settings()
