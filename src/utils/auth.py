from datetime import timedelta, datetime

from fastapi import Request
from passlib.context import CryptContext
from jose import JWTError, jwt
from src.core.settings import settings
from src.schemas.user_schemas import TokenData
from src.utils.exceptions.exceptions import NotAuthorized

pwd_context = CryptContext(
    schemes=["bcrypt"], bcrypt__rounds=12, deprecated="auto"
)


JWT_SECRET_KEY = settings.jwt_secret
JWT_ACCESS_COOKIE_NAME = settings.JWT_ACCESS_COOKIE_NAME
JWT_TOKEN_LOCATION = settings.JWT_TOKEN_LOCATION
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta = None):
    """Создать JWT токен"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(hours=1)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str):
    """Проверить JWT токен"""
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        return TokenData(
            user_id=payload.get("user_id"),
            email=payload.get("email"),
        )
    except JWTError:
        return None


async def get_current_user(request: Request):
    token = request.cookies.get("access_token")

    if not token:
        raise NotAuthorized("Not authenticated")

    token_data = verify_token(token)

    if not token_data:
        raise NotAuthorized("Invalid token")

    return token_data


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(user_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(user_password, hashed_password)
