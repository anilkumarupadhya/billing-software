# services/customer_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
import logging

from models.customer import Customer

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def get_customer(db: Session, customer_id: int) -> Optional[Customer]:
    return db.get(Customer, customer_id)

def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    if not email:
        return None
    return db.query(Customer).filter(Customer.email == email).one_or_none()

def create_customer(db: Session, name: str, gstin: str | None = None, email: str | None = None, phone: str | None = None, address: str | None = None) -> Customer:
    """
    Create a customer. Email uniqueness is enforced if provided.
    """
    if email and get_customer_by_email(db, email):
        raise ServiceError("Customer with this email already exists")
    c = Customer(
        name=name,
        gstin=gstin,
        email=email,
        phone=phone,
        address=address,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(c)
    db.commit()
    db.refresh(c)
    logger.info("Created customer %s (id=%s)", name, c.id)
    return c

def update_customer(db: Session, customer_id: int, *, name: str | None = None, gstin: str | None = None, email: str | None = None, phone: str | None = None, address: str | None = None) -> Customer:
    c = get_customer(db, customer_id)
    if not c:
        raise ServiceError("Customer not found")
    if email and email != c.email:
        # If changing email, ensure uniqueness
        if get_customer_by_email(db, email):
            raise ServiceError("Customer with this email already exists")
        c.email = email
    if name is not None:
        c.name = name
    if gstin is not None:
        c.gstin = gstin
    if phone is not None:
        c.phone = phone
    if address is not None:
        c.address = address
    c.updated_at = datetime.utcnow()
    db.add(c)
    db.commit()
    db.refresh(c)
    logger.info("Updated customer id=%s", c.id)
    return c

def delete_customer(db: Session, customer_id: int) -> None:
    c = get_customer(db, customer_id)
    if not c:
        raise ServiceError("Customer not found")
    db.delete(c)
    db.commit()
    logger.info("Deleted customer id=%s", customer_id)

def list_customers(db: Session, q: str | None = None, page: int = 1, page_size: int = 25) -> dict:
    """
    Return paginated customers and total count.
    """
    stmt = select(Customer)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(
            func.lower(Customer.name).like(pattern) |
            func.lower(Customer.email).like(pattern) |
            func.lower(Customer.gstin).like(pattern) |
            func.lower(Customer.phone).like(pattern)
        )
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return {"total": total, "items": items}
