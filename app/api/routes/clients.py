"""Client routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.db.models.client import Client
from app.schemas.models import Client as ClientSchema
from app.schemas.models import ClientCreate, TokenPayload

router = APIRouter()


@router.get("/", response_model=list[ClientSchema])
def list_clients(
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> list[ClientSchema]:
    """List clients for the account."""

    clients = db.query(Client).filter(Client.account_id == token.account_id).all()
    return [ClientSchema.model_validate(client) for client in clients]


@router.post("/", response_model=ClientSchema, status_code=status.HTTP_201_CREATED)
def create_client(
    payload: ClientCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> ClientSchema:
    """Create a new client."""

    if payload.account_id != token.account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid account")
    client = Client(**payload.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return ClientSchema.model_validate(client)


@router.get("/{client_id}", response_model=ClientSchema)
def get_client(
    client_id: int,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> ClientSchema:
    client = db.query(Client).filter(Client.id == client_id, Client.account_id == token.account_id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return ClientSchema.model_validate(client)
