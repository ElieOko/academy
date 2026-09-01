from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=str(ENV_FILE), extra="ignore")

    database_url: str
    secret_key: str
    admin_email: str = "admin@acad-emy.com"
    admin_password: str = "AcadEmy243!"
    cors_origins: str = (
        "http://127.0.0.1:4321,"
        "http://localhost:4321,"
        "http://acad-emy.com,"
        "http://www.acad-emy.com,"
        "https://acad-emy.com,"
        "https://www.acad-emy.com"
    )
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7

    @property
    def origins(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
