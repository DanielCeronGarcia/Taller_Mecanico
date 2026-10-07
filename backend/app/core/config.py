from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./taller.db"
    jwt_secret: str = "solo-desarrollo-cambie-esta-clave"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 60
    first_admin_email: str = "admin@taller.example.com"
    first_admin_password: str = "CambieEstaClave123!"
    frontend_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origins(self) -> list[str]:
        return [origin.strip() for origin in self.frontend_origins.split(",")]


@lru_cache
def get_settings() -> Settings:
    return Settings()
