"""Tests for the LLM agent stubs."""

from app.llm_agent import call_tool, parse_intent


def test_parse_intent_routes_messages() -> None:
    assert parse_intent("What times are available?") == "check_availability"
    assert parse_intent("Can we book it?") == "create_appointment"
    assert parse_intent("How do I pay?") == "collect_payment"


def test_call_tool_dispatches() -> None:
    result = call_tool("send_message", {"to": "+15551234567", "body": "Hello"})
    assert result["status"] == "sent"

    appointment = call_tool("create_appointment", {"client_id": 1, "service_id": 2, "provider_id": 3})
    assert appointment["service_id"] == 2
