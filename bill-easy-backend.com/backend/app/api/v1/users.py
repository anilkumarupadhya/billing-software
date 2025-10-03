from datetime import datetime
from typing import Optional, List, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from core.security import decode_access_token, hash_password
from db.session import get_db
from models.user import User

router = APIRouter(prefix="/api/v1/users", tags=["Users"])
auth_scheme = HTTPBearer(auto_error=True)

# ---------------------------
# Auth & RBAC dependencies
# ---------------------------
class CurrentUser(BaseModel):
    sub: EmailStr
    role: Literal["admin", "staff", "customer"]

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> CurrentUser:
    payload = decode_access_token(creds.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return CurrentUser(sub=payload.get("sub"), role=payload.get("role"))

def require_roles(*roles: str):
    def _dep(u: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if u.role not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return u
    return _dep

# ---------------------------
# Schemas
# ---------------------------
class UserCreate(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    password: str = Field(min_length=8)
    role: Literal["admin", "staff", "customer"] = "staff"

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    password: Optional[str] = Field(default=None, min_length=8)
    role: Optional[Literal["admin", "staff", "customer"]] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class PaginatedUsers(BaseModel):
    total: int
    items: List[UserOut]

# ---------------------------
# Helpers
# ---------------------------
def ensure_unique_email(db: Session, email: str, exclude_user_id: Optional[int] = None):
    q = select(User).where(User.email == email)
    user = db.scalar(q)
    if user and (exclude_user_id is None or user.id != exclude_user_id):
        raise HTTPException(status_code=400, detail="Email already in use")

# ---------------------------
# Routes
# ---------------------------
@router.get("", response_model=PaginatedUsers)
def list_users(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin")),
    q: Optional[str] = Query(default=None, description="Search by email/full_name"),
    sort: Literal["created_at", "-created_at", "email", "-email"] = "created_at",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    stmt = select(User)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(User.email).like(pattern) | func.lower(User.full_name).like(pattern))

    if sort in ("created_at", "email"):
        stmt = stmt.order_by(getattr(User, sort).asc())
    elif sort in ("-created_at", "-email"):
        stmt = stmt.order_by(getattr(User, sort[1:]).desc())

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return PaginatedUsers(total=total or 0, items=items)

@router.post("", response_model=UserOut, status_code=201)
def create_user(payload: UserCreate, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    ensure_unique_email(db, payload.email)
    user = User(
        email=payload.email,
        full_name=payload.full_name or "",
        role=payload.role,
        hashed_password=hash_password(payload.password),
        is_active=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), cu: CurrentUser = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # Allow self-read or admin
    if cu.role != "admin" and cu.sub != user.email:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db), cu: CurrentUser = Depends(get_current_user)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Allow self-update (except role/is_active) or admin
    if cu.role != "admin" and cu.sub != user.email:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    if payload.full_name is not None:
        user.full_name = payload.full_name
    if payload.password:
        user.hashed_password = hash_password(payload.password)

    # Only admin can change role or is_active
    if cu.role == "admin":
        if payload.role is not None:
            user.role = payload.role
        if payload.is_active is not None:
            user.is_active = payload.is_active

    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}", status_code=204)
def deactivate_user(user_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    user.updated_at = datetime.utcnow()
    db.add(user)
    db.commit()
    return
