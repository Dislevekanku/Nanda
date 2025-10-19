"""Appointment routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.db.models.appointment import Appointment
from app.schemas.models import Appointment as AppointmentSchema
from app.schemas.models import AppointmentCreate, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[AppointmentSchema])
def list_appointments(
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> list[AppointmentSchema]:
    appointments = db.query(Appointment).filter(Appointment.account_id == token.account_id).all()
    return [AppointmentSchema.model_validate(appointment) for appointment in appointments]


@router.post("/", response_model=AppointmentSchema, status_code=status.HTTP_201_CREATED)
def create_appointment(
    payload: AppointmentCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> AppointmentSchema:
    if payload.account_id != token.account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid account")
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return AppointmentSchema.model_validate(appointment)
