from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    APP_NAME: str = "github-org-integration"
    APP_ENV: str = "dev"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_DEBUG: bool = True

    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB: str = "github_integration"
    GITHUB_CLIENT_ID: str = ""
    GITHUB_CLIENT_SECRET: str = ""
    GITHUB_OAUTH_CALLBACK: str = "http://localhost:8000/auth/github/callback"
    GITHUB_WEBHOOK_SECRET: str = ""
    GITHUB_API_BASE: str = "https://api.github.com"

    ENCRYPTION_KEY: str = "replace_with_a_32_char_key"


settings = Settings()
