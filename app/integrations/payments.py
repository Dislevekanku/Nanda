"""Stripe integration stub."""

from typing import Any, Dict


def create_payment_intent(amount_cents: int, currency: str = "usd") -> Dict[str, Any]:
    """Return fake payment intent information."""

    return {
        "id": "pi_test_123",
        "amount": amount_cents,
        "currency": currency,
        "status": "requires_confirmation",
    }
