from datetime import datetime
from typing import Optional, List, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from core.security import decode_access_token
from db.session import get_db
from models.customer import Customer

router = APIRouter(prefix="/api/v1/customers", tags=["Customers"])
auth_scheme = HTTPBearer(auto_error=True)

# ---------- Auth & RBAC ----------
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

# ---------- Schemas ----------
class CustomerIn(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    phone: str
    gst_no: Optional[str] = None
    shipping_address: str
    billing_address: str
    eway: Optional[str] = None

class CustomerOut(CustomerIn):
    id: int

    class Config:
        from_attributes = True

class PaginatedCustomers(BaseModel):
    total: int
    items: List[CustomerOut]

# ---------- Routes ----------
@router.get("", response_model=PaginatedCustomers)
def list_customers(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin", "staff")),
    q: Optional[str] = Query(default=None, description="Search by name/gstin/email/phone"),
    sort: Literal["created_at", "-created_at", "name", "-name"] = "name",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    stmt = select(Customer)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(
            func.lower(Customer.name).like(pattern)
            | func.lower(Customer.gst_no).like(pattern)
            | func.lower(Customer.email).like(pattern)
            | func.lower(Customer.phone).like(pattern)
        )
    if sort in ("created_at", "name"):
        stmt = stmt.order_by(getattr(Customer, sort).asc())
    elif sort in ("-created_at", "-name"):
        stmt = stmt.order_by(getattr(Customer, sort[1:]).desc())

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return PaginatedCustomers(total=total or 0, items=items)

@router.post("", response_model=CustomerOut, status_code=201)
def create_customer(payload: CustomerIn, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    customer = Customer(
        name=payload.name,
        email=payload.email,
        phone=payload.phone,
        gst_no=payload.gst_no,
        shipping_address=payload.shipping_address,
        billing_address=payload.billing_address,
        eway=payload.eway,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(customer)
    db.commit()
    db.refresh(customer)
    return customer

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    return c

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerIn, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    c.name = payload.name
    c.email = payload.email
    c.phone = payload.phone
    c.gst_no = payload.gst_no
    c.shipping_address = payload.shipping_address
    c.billing_address = payload.billing_address
    c.eway = payload.eway
    c.updated_at = datetime.utcnow()
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    c = db.get(Customer, customer_id)
    if not c:
        raise HTTPException(status_code=404, detail="Customer not found")
    db.delete(c)
    db.commit()
    return

