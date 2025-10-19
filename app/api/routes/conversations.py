"""Conversation routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.db.models.conversation import Conversation
from app.db.models.message import Message
from app.schemas.models import Conversation as ConversationSchema
from app.schemas.models import ConversationCreate, Message as MessageSchema
from app.schemas.models import MessageCreate, TokenPayload
from app.state_machine import next_state

router = APIRouter()


@router.get("/", response_model=list[ConversationSchema])
def list_conversations(
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> list[ConversationSchema]:
    conversations = db.query(Conversation).filter(Conversation.account_id == token.account_id).all()
    return [ConversationSchema.model_validate(conversation) for conversation in conversations]


@router.post("/", response_model=ConversationSchema, status_code=status.HTTP_201_CREATED)
def create_conversation(
    payload: ConversationCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> ConversationSchema:
    if payload.account_id != token.account_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid account")
    conversation = Conversation(**payload.model_dump())
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return ConversationSchema.model_validate(conversation)


@router.post("/{conversation_id}/messages", response_model=MessageSchema, status_code=status.HTTP_201_CREATED)
def add_message(
    conversation_id: int,
    payload: MessageCreate,
    token: TokenPayload = Depends(get_current_account),
    db: Session = Depends(get_db),
) -> MessageSchema:
    conversation = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.account_id == token.account_id)
        .first()
    )
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    message = Message(**payload.model_dump())
    if message.conversation_id != conversation.id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Conversation mismatch")

    conversation.last_agent_state = next_state(conversation, message)
    db.add(message)
    db.commit()
    db.refresh(message)
    return MessageSchema.model_validate(message)
