"""Service routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.db.models.service import Service
from app.schemas.models import Service as ServiceSchema
from app.schemas.models import ServiceCreate, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[ServiceSchema])
def list_services(
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> list[ServiceSchema]:
    services = db.query(Service).filter(Service.account_id == token.account_id).all()
    return [ServiceSchema.model_validate(service) for service in services]


@router.post("/", response_model=ServiceSchema, status_code=status.HTTP_201_CREATED)
def create_service(
    payload: ServiceCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> ServiceSchema:
    if payload.account_id != token.account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid account")
    service = Service(**payload.model_dump())
    db.add(service)
    db.commit()
    db.refresh(service)
    return ServiceSchema.model_validate(service)
