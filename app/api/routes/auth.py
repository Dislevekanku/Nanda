"""Authentication routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_current_account, get_db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.db.models.account import Account
from app.db.models.staff import Staff
from app.schemas.models import AccountCreate, StaffCreate, Token, TokenPayload

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


@router.post("/signup", response_model=Token)
def signup(payload: StaffCreate, db: Session = Depends(get_db)) -> Token:
    """Create a new account and staff member."""

    existing_staff = db.query(Staff).filter(Staff.email == payload.email).first()
    if existing_staff:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    account = None
    if payload.account_id:
        account = db.query(Account).filter(Account.id == payload.account_id).first()

    if not account:
        account_data = AccountCreate(name="Glow MedSpa")
        account = Account(name=account_data.name)
        db.add(account)
        db.flush()

    staff_member = Staff(
        account_id=account.id,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        role=payload.role,
        password_hash=get_password_hash(payload.password),
    )
    db.add(staff_member)
    db.commit()
    db.refresh(staff_member)

    token = create_access_token({"account_id": account.id, "staff_id": staff_member.id})
    return Token(access_token=token)


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    """Authenticate a staff member and return a token."""

    staff_member = db.query(Staff).filter(Staff.email == form_data.username).first()
    if not staff_member or not verify_password(form_data.password, staff_member.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"account_id": staff_member.account_id, "staff_id": staff_member.id})
    return Token(access_token=token)


@router.get("/me")
def read_current_staff(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> dict:
    """Return information about the current staff member."""

    payload: TokenPayload = get_current_account(token=token, db=db)
    staff_member = db.query(Staff).filter(Staff.id == payload.staff_id).first()
    if not staff_member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return {
        "id": staff_member.id,
        "email": staff_member.email,
        "first_name": staff_member.first_name,
        "last_name": staff_member.last_name,
        "role": staff_member.role,
    }
