from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import config


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    if expires_delta:
        expire = datetime.now(UTC) + expires_delta
    else:
        expire = datetime.now(UTC) + timedelta(seconds=config.secure.JWT_ACCESS_TTL_SECONDS)

    to_encode = {"sub": str(subject), "exp": expire, "type": "access"}
    encoded_jwt = jwt.encode(to_encode, config.secure.JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def create_refresh_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(seconds=config.secure.JWT_REFRESH_TTL_SECONDS)
    to_encode = {"sub": str(subject), "exp": expire, "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, config.secure.JWT_SECRET, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, config.secure.JWT_SECRET, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        return {}
    except jwt.InvalidTokenError:
        return {}
    except Exception:
        return {}
