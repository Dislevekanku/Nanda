"""Security helpers for password hashing and token creation."""

from __future__ import annotations

import base64
import hashlib
import hmac
import os
from datetime import datetime, timedelta

from app.core import jwt
from app.core.config import settings

_ITERATIONS = 390000


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Create a signed JWT token."""

    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=1))
    to_encode.update({"exp": int(expire.timestamp())})
    return jwt.encode(to_encode, settings.secret_key)


def get_password_hash(password: str) -> str:
    """Hash a password using PBKDF2."""

    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, _ITERATIONS)
    return f"{_ITERATIONS}${base64.b64encode(salt).decode()}${base64.b64encode(key).decode()}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a PBKDF2 password hash."""

    try:
        iterations_str, salt_b64, key_b64 = hashed_password.split("$")
        iterations = int(iterations_str)
    except ValueError:  # pragma: no cover - invalid hash format
        return False
    salt = base64.b64decode(salt_b64)
    expected_key = base64.b64decode(key_b64)
    candidate_key = hashlib.pbkdf2_hmac("sha256", plain_password.encode("utf-8"), salt, iterations)
    return hmac.compare_digest(candidate_key, expected_key)
