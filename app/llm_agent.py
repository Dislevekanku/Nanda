"""LLM agent scaffolding."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, Dict

from app.services import (
    create_appointment,
    create_payment_intent,
    search_availability,
    send_message,
)

TOOLS: dict[str, Callable[..., Any]] = {
    "search_availability": search_availability,
    "create_appointment": create_appointment,
    "send_message": send_message,
    "create_payment": create_payment_intent,
}


def parse_intent(message_text: str) -> str:
    """Very small heuristic to infer intent."""

    text = message_text.lower()
    if "availability" in text or "time" in text:
        return "check_availability"
    if "book" in text or "schedule" in text:
        return "create_appointment"
    if "pay" in text or "card" in text:
        return "collect_payment"
    return "general_inquiry"


def call_tool(tool_name: str, params: Dict[str, Any]) -> Any:
    """Call a tool from the registry."""

    tool = TOOLS.get(tool_name)
    if not tool:
        raise ValueError(f"Tool '{tool_name}' not found")
    return tool(**params)
