from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NZ Product Opportunity Scanner"
    environment: str = "development"

    database_url: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/opportunity_scanner"
    redis_url: str = "redis://localhost:6379/0"

    llm_api_key: str | None = None
    llm_model: str = "gpt-4o-mini"

    google_trends_api_key: str | None = None
    tiktok_api_key: str | None = None
    trade_me_consumer_key: str | None = None
    trade_me_consumer_secret: str | None = None
    aliexpress_api_key: str | None = None
    serpapi_key: str | None = None

    trends_provider: str = "mock"
    social_provider: str = "mock"
    marketplace_provider: str = "mock"
    supplier_provider: str = "mock"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


settings = Settings()
