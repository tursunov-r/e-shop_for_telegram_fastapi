import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    jwt_secret: str
    JWT_ACCESS_COOKIE_NAME: str
    JWT_TOKEN_LOCATION: list[str]
    cors_origins: list[str] = [
        "http://localhost:3000",
        "https://sfmshop.example.ru",
    ]
    rate_limit_login: str = "5/minute"

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
