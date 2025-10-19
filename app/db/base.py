"""Declarative base and model imports for Alembic."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base class."""

    pass


# Import models to register with SQLAlchemy metadata.
from app.db.models import account, appointment, automation_event, client, conversation, message, service, staff  # noqa: E402,F401
