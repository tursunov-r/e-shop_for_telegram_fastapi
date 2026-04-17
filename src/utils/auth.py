from passlib.context import CryptContext
from authx import AuthX, AuthXConfig
from src.core.settings import settings

pwd_context = CryptContext(
    schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto"
)


config = AuthXConfig()
config.JWT_SECRET_KEY = settings.jwt_secret
config.JWT_ACCESS_COOKIE_NAME = settings.JWT_ACCESS_COOKIE_NAME
config.JWT_TOKEN_LOCATION = settings.JWT_TOKEN_LOCATION

security = AuthX(config=config)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(user_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(user_password, hashed_password)
