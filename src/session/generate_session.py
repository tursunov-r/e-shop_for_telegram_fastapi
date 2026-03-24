import secrets


def generate_user_session(length: int = 30) -> str:
    return secrets.token_hex(length)
