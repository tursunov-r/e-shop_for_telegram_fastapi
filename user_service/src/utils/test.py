from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Хешировать пароль через bcrypt."""
    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """Проверить пароль по хешу."""
    return pwd_context.verify(plain_password, hashed_password)


# Пример
hashed = hash_password("my_secret_password")
print(hashed)
# $2b$12$LJ3m4ys3Lg2nkBfQJHMXYO...

print(verify_password("my_secret_password", hashed))
# True
print(verify_password("wrong_password", hashed))
# False
