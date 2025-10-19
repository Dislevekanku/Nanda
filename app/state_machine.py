"""Conversation state machine for the MedSpa agent."""

from enum import Enum

from app.db.models.conversation import Conversation
from app.db.models.message import Message


class AgentState(str, Enum):
    NEEDS_SERVICE = "needs_service"
    NEEDS_TIME = "needs_time"
    NEEDS_DETAILS = "needs_details"
    NEEDS_PAYMENT = "needs_payment"
    BOOKED = "booked"


def next_state(conversation: Conversation, message: Message) -> str:
    """Determine the next agent state from a message."""

    content = message.content.lower()
    if "book" in content or "scheduled" in content:
        return AgentState.BOOKED.value
    if "payment" in content or "card" in content:
        return AgentState.NEEDS_PAYMENT.value
    if "friday" in content or "time" in content or "week" in content:
        return AgentState.NEEDS_TIME.value
    if "details" in content or "info" in content:
        return AgentState.NEEDS_DETAILS.value
    if "botox" in content or "service" in content:
        return AgentState.NEEDS_SERVICE.value
    return conversation.last_agent_state or AgentState.NEEDS_SERVICE.value
