"""Test the conversation state machine."""

from types import SimpleNamespace

from app.state_machine import AgentState, next_state


def test_state_machine_progression() -> None:
    convo = SimpleNamespace(last_agent_state=None)

    state = next_state(convo, SimpleNamespace(content="I want Botox"))
    assert state == AgentState.NEEDS_SERVICE.value
    convo.last_agent_state = state

    state = next_state(convo, SimpleNamespace(content="next week works"))
    assert state == AgentState.NEEDS_TIME.value
    convo.last_agent_state = state

    state = next_state(convo, SimpleNamespace(content="Friday 5 pm is perfect"))
    assert state == AgentState.NEEDS_TIME.value

    state = next_state(convo, SimpleNamespace(content="Payment details"))
    assert state == AgentState.NEEDS_PAYMENT.value
