"""Pydantic models representing database entities."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    name: str


class AccountCreate(AccountBase):
    pass


class Account(AccountBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class StaffBase(BaseModel):
    account_id: int | None = None
    email: str
    first_name: str
    last_name: str
    role: str


class StaffCreate(StaffBase):
    password: str


class Staff(StaffBase):
    id: int
    account_id: int
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ServiceBase(BaseModel):
    account_id: int
    name: str
    description: str | None = None
    duration_minutes: int
    price_cents: int


class ServiceCreate(ServiceBase):
    pass


class Service(ServiceBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ClientBase(BaseModel):
    account_id: int
    email: str | None = None
    first_name: str
    last_name: str
    phone_number: str | None = None


class ClientCreate(ClientBase):
    pass


class Client(ClientBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class AppointmentBase(BaseModel):
    account_id: int
    service_id: int
    client_id: int
    staff_id: int
    start_time: datetime
    end_time: datetime
    status: str


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationBase(BaseModel):
    account_id: int
    client_id: int
    topic: str | None = None
    last_agent_state: str | None = None


class ConversationCreate(ConversationBase):
    pass


class Conversation(ConversationBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class MessageBase(BaseModel):
    conversation_id: int
    sender: str
    content: str
    tool_invocation: dict | None = None


class MessageCreate(MessageBase):
    pass


class Message(MessageBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class AutomationEventBase(BaseModel):
    account_id: int
    name: str
    payload: dict
    status: str


class AutomationEventCreate(AutomationEventBase):
    pass


class AutomationEvent(AutomationEventBase):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    account_id: int
    staff_id: int
    exp: Optional[int] = None
