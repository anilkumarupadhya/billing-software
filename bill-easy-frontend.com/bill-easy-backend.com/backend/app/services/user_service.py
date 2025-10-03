# services/user_service.py
from datetime import datetime
from sqlalchemy.orm import Session
import logging

from models.user import User
from core.security import hash_password
from core.utils import to_ist

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def get_user_by_id(db: Session, user_id: int) -> User:
    return db.get(User, user_id)

def authenticate_user(db: Session, email: str, password: str) -> dict | None:
    """
    Verify credentials and return user data with updated_at/created_at in IST.
    Returns None if authentication fails.
    """
    user = get_user_by_email(db, email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    if not user.is_active:
        return None

    # Return dict with IST datetime
    user_data = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "updated_at": to_ist(user.updated_at),
        "created_at": to_ist(user.created_at),
    }
    return user_data


    
def create_user(db: Session, *, email: str, full_name: str, password: str, role: str = "Staff", is_active: bool = True) -> dict:
    """
    Create a new user and return dict with updated_at/created_at in IST.
    """
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise ServiceError("Email already registered")

    hashed_pwd = hash_password(password)
    now_utc = datetime.utcnow()

    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed_pwd,
        role=role,
        is_active=is_active,
        created_at=now_utc,
        updated_at=now_utc
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Created new user %s", user.email)

    # Convert UTC timestamps to IST for response
    user_data = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": to_ist(user.created_at),
        "updated_at": to_ist(user.updated_at)
    }

    return user_data

def update_user(db: Session, user_id: int, *, full_name: str | None = None, password: str | None = None, role: str | None = None, is_active: bool | None = None) -> dict:
    """
    Update a user in DB, return dict with updated_at converted to IST.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise ServiceError("User not found")

    if full_name is not None:
        user.full_name = full_name
    if password:
        user.hashed_password = hash_password(password)
    if role is not None:
        user.role = role
    if is_active is not None:
        user.is_active = is_active

    user.updated_at = datetime.utcnow()  # stored in UTC
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Updated user %s", user.email)

    # Convert updated_at to IST for response
    user_data = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "updated_at": to_ist(user.updated_at),
        "created_at": to_ist(user.created_at),
    }
    return user_data

def deactivate_user(db: Session, user_id: int) -> dict:
    """
    Deactivate user and return dict with updated_at in IST.
    """
    user = get_user_by_id(db, user_id)
    if not user:
        raise ServiceError("User not found")

    user.is_active = False
    user.updated_at = datetime.utcnow()  # still UTC in DB
    db.add(user)
    db.commit()
    db.refresh(user)

    logger.info("Deactivated user %s", user.email)

    user_data = {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "updated_at": to_ist(user.updated_at),
        "created_at": to_ist(user.created_at),
    }
    return user_data
