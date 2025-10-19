"""Twilio integration stub."""

from typing import Any, Dict


def send_message(to: str, body: str) -> Dict[str, Any]:
    """Pretend to send an SMS message."""

    return {"sid": "SM123", "to": to, "body": body, "status": "sent"}
