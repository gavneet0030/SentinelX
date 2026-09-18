from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "SentinelX"
    app_version: str = "0.1.0"
    environment: str = "development"

    api_host: str = "0.0.0.0"
    api_port: int = 8000

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "sentinelx"
    postgres_user: str = "sentinelx"
    postgres_password: str = "sentinelx"

    redis_host: str = "localhost"
    redis_port: int = 6379

    kafka_bootstrap_servers: str = "localhost:9092"

    model_name: str = "sentinelx-baseline"
    model_version: str = "0.1.0"

    risk_approve_threshold: float = 0.30
    risk_review_threshold: float = 0.70

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
