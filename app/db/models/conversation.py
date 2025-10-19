"""Conversation model."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Conversation(Base):
    """Represents a client conversation."""

    __tablename__ = "convo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id", ondelete="CASCADE"), nullable=False, index=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("client.id", ondelete="CASCADE"), nullable=False)
    appointment_id: Mapped[Optional[int]] = mapped_column(ForeignKey("appointment.id", ondelete="SET NULL"), nullable=True)
    topic: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_agent_state: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    account: Mapped["Account"] = relationship("Account")
    client: Mapped["Client"] = relationship("Client", back_populates="conversations")
    appointment: Mapped[Optional["Appointment"]] = relationship("Appointment", back_populates="conversation")
    messages: Mapped[list["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
