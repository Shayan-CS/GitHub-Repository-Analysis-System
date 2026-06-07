from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "GitHub Engineering Assistant"
    debug: bool = True

    # Async DB URL; override via environment in production/dev
    database_url: str = "sqlite+aiosqlite:///./dev.db"
    github_token: str | None = None


settings = Settings()
