"""Automation routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.db.models.automation_event import AutomationEvent
from app.schemas.models import AutomationEvent as AutomationEventSchema
from app.schemas.models import AutomationEventCreate, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[AutomationEventSchema])
def list_automation_events(
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> list[AutomationEventSchema]:
    events = db.query(AutomationEvent).filter(AutomationEvent.account_id == token.account_id).all()
    return [AutomationEventSchema.model_validate(event) for event in events]


@router.post("/", response_model=AutomationEventSchema, status_code=status.HTTP_201_CREATED)
def create_automation_event(
    payload: AutomationEventCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> AutomationEventSchema:
    if payload.account_id != token.account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid account")
    event = AutomationEvent(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return AutomationEventSchema.model_validate(event)
