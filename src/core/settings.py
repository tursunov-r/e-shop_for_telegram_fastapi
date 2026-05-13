import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "<PASSWORD>"
    DB_NAME: str = "SFMShop"

    jwt_secret: str = "your-jwt-secret"
    JWT_ACCESS_COOKIE_NAME: str = "jwt"
    JWT_TOKEN_LOCATION: list[str] = ["cookies"]
    cors_origins: list[str] = [
        "http://localhost:3000",
        "https://sfmshop.example.ru",
    ]
    rate_limit_login: str = "5/minute"

    exchangerate_api_com_key: str = "<KEY>"
    exchangerates_api_io_key: str = "<KEY>"
    openexchangerates_org_key: str = "<KEY>"

    @property
    def db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

    @property
    def pool_url(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
