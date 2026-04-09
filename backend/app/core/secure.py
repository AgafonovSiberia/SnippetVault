from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import config


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    expire = datetime.now(UTC) + (
        expires_delta or timedelta(seconds=config.secure.JWT_ACCESS_TTL_SECONDS)
    )
    return jwt.encode(
        {"sub": str(subject), "exp": expire, "type": "access"},
        config.secure.JWT_SECRET,
        algorithm="HS256",
    )


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(seconds=config.secure.JWT_REFRESH_TTL_SECONDS)
    return jwt.encode(
        {"sub": str(subject), "exp": expire, "type": "refresh"},
        config.secure.JWT_SECRET,
        algorithm="HS256",
    )


def decode_token(token: str) -> dict | None:
    """Декодировать JWT. Возвращает None при любой ошибке."""
    try:
        return jwt.decode(token, config.secure.JWT_SECRET, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
