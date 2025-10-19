"""Service layer for the agent."""

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from app.integrations.calendar import search_availability
from app.integrations.payments import create_payment_intent
from app.integrations.sms import send_message


def create_appointment(client_id: int, service_id: int, provider_id: int) -> Dict[str, Any]:
    """Mock appointment creation."""

    start = datetime.now(timezone.utc) + timedelta(days=1)
    return {
        "appointment_id": 999,
        "client_id": client_id,
        "service_id": service_id,
        "provider_id": provider_id,
        "start_time": start.isoformat(),
    }


__all__ = [
    "search_availability",
    "create_payment_intent",
    "send_message",
    "create_appointment",
]
