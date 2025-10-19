"""Common dependencies for API routers."""

from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import jwt
from app.core.config import settings
from app.db.session import SessionLocal
from app.schemas.models import TokenPayload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_db() -> Generator[Session, None, None]:
    """Yield a database session and ensure it is closed."""

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_account(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> TokenPayload:
    """Decode the provided token and return the payload."""

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key)
        token_data = TokenPayload.model_validate(payload)
    except jwt.JWTError as exc:  # pragma: no cover - defensive branch
        raise credentials_exception from exc

    from app.db.models.account import Account  # local import to avoid cycles

    account = db.query(Account).filter(Account.id == token_data.account_id).first()
    if not account:
        raise credentials_exception
    return token_data
