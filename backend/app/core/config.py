from functools import lru_cache
import os

from pydantic import BaseModel, Field


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


class Settings(BaseModel):
    app_name: str = "Athena AI Risk Terminal"
    service_name: str = "athena-backend"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"
    api_prefix: str = "/api"
    database_url: str = "sqlite+pysqlite:///./athena_dev.db"
    redis_url: str = "redis://localhost:6379/0"
    secret_key: str = "athena-dev-secret"
    athena_ai_provider: str = "fallback"
    athena_ai_model: str | None = None
    openai_api_key: str | None = None
    allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ],
    )


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "Athena AI Risk Terminal"),
        service_name=os.getenv("SERVICE_NAME", "athena-backend"),
        app_env=os.getenv("APP_ENV", "development"),
        debug=os.getenv("DEBUG", "true").lower() in {"1", "true", "yes", "on"},
        log_level=os.getenv("LOG_LEVEL", "INFO"),
        api_prefix=os.getenv("API_PREFIX", "/api"),
        database_url=os.getenv(
            "ATHENA_DATABASE_URL",
            os.getenv("DATABASE_URL", "sqlite+pysqlite:///./athena_dev.db"),
        ),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        secret_key=os.getenv("SECRET_KEY", "athena-dev-secret"),
        athena_ai_provider=os.getenv("ATHENA_AI_PROVIDER", "fallback"),
        athena_ai_model=os.getenv("ATHENA_AI_MODEL"),
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        allowed_origins=_parse_csv(
            os.getenv(
                "BACKEND_CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173",
            ),
        ),
    )


settings = get_settings()
