"""Minimal JWT utilities to avoid external dependencies."""

from __future__ import annotations

import base64
import json
import time
from dataclasses import dataclass
from typing import Any, Dict

from hashlib import sha256
import hmac


@dataclass
class JWTError(Exception):
    """Exception raised for JWT parsing errors."""

    message: str

    def __str__(self) -> str:  # pragma: no cover - simple string repr
        return self.message


def _urlsafe_b64encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _urlsafe_b64decode(data: str) -> bytes:
    padding = '=' * (-len(data) % 4)
    return base64.urlsafe_b64decode(data + padding)


def encode(payload: Dict[str, Any], secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    header_segment = _urlsafe_b64encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_segment = _urlsafe_b64encode(json.dumps(payload, default=str, separators=(",", ":")).encode("utf-8"))
    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), signing_input, sha256).digest()
    signature_segment = _urlsafe_b64encode(signature)
    return f"{header_segment}.{payload_segment}.{signature_segment}"


def decode(token: str, secret: str) -> Dict[str, Any]:
    try:
        header_segment, payload_segment, signature_segment = token.split(".")
    except ValueError as exc:  # pragma: no cover - invalid token shape
        raise JWTError("Invalid token") from exc

    signing_input = f"{header_segment}.{payload_segment}".encode("utf-8")
    expected_signature = hmac.new(secret.encode("utf-8"), signing_input, sha256).digest()
    actual_signature = _urlsafe_b64decode(signature_segment)
    if not hmac.compare_digest(expected_signature, actual_signature):
        raise JWTError("Signature verification failed")

    payload_bytes = _urlsafe_b64decode(payload_segment)
    payload: Dict[str, Any] = json.loads(payload_bytes)

    exp = payload.get("exp")
    if exp is not None and time.time() > int(exp):
        raise JWTError("Token has expired")

    return payload
