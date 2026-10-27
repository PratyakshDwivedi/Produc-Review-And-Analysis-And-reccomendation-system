"""Password hashing and JWT helpers."""
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import JWTError, jwt

from backend import config


def hash_password(password: str) -> str:
    # bcrypt operates on at most 72 bytes.
    return bcrypt.hashpw(password.encode("utf-8")[:72], bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False


def create_token(subject: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRE_MINUTES)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, config.JWT_SECRET, algorithm=config.JWT_ALGORITHM)


def decode_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=[config.JWT_ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
