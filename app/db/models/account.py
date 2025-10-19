"""Account model."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Account(Base):
    """Represents a MedSpa business account."""

    __tablename__ = "account"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    staff: Mapped[list["Staff"]] = relationship("Staff", back_populates="account", cascade="all, delete-orphan")
    services: Mapped[list["Service"]] = relationship("Service", back_populates="account", cascade="all, delete-orphan")
    clients: Mapped[list["Client"]] = relationship("Client", back_populates="account", cascade="all, delete-orphan")
    appointments: Mapped[list["Appointment"]] = relationship("Appointment", back_populates="account", cascade="all, delete-orphan")
    automation_events: Mapped[list["AutomationEvent"]] = relationship(
        "AutomationEvent", back_populates="account", cascade="all, delete-orphan"
    )
