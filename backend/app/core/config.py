from pydantic import model_validator, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    PROJECT_NAME: str = "SnippetVault"
    API_V1_STR: str = "/api/v1"
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://localhost:5173",
        "https://127.0.0.1:5173",
        "http://localhost:8000",
    ]


class SecureSettings(BaseSettings):
    JWT_SECRET: str
    JWT_ACCESS_TTL_SECONDS: int = 900       # 15 минут
    JWT_REFRESH_TTL_SECONDS: int = 2592000  # 30 дней

    model_config = SettingsConfigDict(env_prefix="SECURE_")


class ProviderSettings(BaseSettings):
    YANDEX_CLIENT_ID: str = ""
    YANDEX_CLIENT_SECRET: str = ""
    YANDEX_REDIRECT_URI: str = ""

    model_config = SettingsConfigDict(env_prefix="PROVIDER_")


class DatabaseSettings(BaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DB_URL: PostgresDsn | None = None

    @model_validator(mode="after")
    def assemble_db_url(self) -> "DatabaseSettings":
        if self.DB_URL is None:
            self.DB_URL = PostgresDsn.build(
                scheme="postgresql+asyncpg",
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                path=self.POSTGRES_DB,
            )
        return self


class Config(BaseSettings):
    app: AppSettings = AppSettings()
    secure: SecureSettings = SecureSettings()
    provider: ProviderSettings = ProviderSettings()
    database: DatabaseSettings = DatabaseSettings()


config = Config()
