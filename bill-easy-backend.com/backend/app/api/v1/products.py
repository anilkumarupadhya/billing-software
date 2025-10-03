from datetime import datetime
from typing import Optional, List, Literal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, condecimal
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from core.security import decode_access_token
from db.session import get_db
from models.product import Product

router = APIRouter(prefix="/api/v1/products", tags=["Products"])
auth_scheme = HTTPBearer(auto_error=True)

# ---------- Auth & RBAC ----------
class CurrentUser(BaseModel):
    sub: str
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
class ProductIn(BaseModel):
    name: str
    code: Optional[str] = None
    hsn_sac: Optional[str] = None
    price: condecimal(gt=-0.0001) = 0  # non-negative
    tax_rate: condecimal(ge=0, le=100) = 0
    discount: condecimal(ge=0, le=100) = 0

class ProductOut(ProductIn):
    id: int

    class Config:
        from_attributes = True

class PaginatedProducts(BaseModel):
    total: int
    items: List[ProductOut]

# ---------- Helpers ----------
def ensure_unique_product(db: Session, name: str, code: Optional[str], exclude_id: Optional[int] = None):
    stmt = select(Product).where(func.lower(Product.name) == name.lower())
    if code:
        stmt = stmt.union_all(select(Product).where(func.lower(Product.code) == code.lower()))
    rows = db.execute(stmt).scalars().all()
    for p in rows:
        if exclude_id is None or p.id != exclude_id:
            raise HTTPException(status_code=400, detail="Product with same name or code already exists")

# ---------- Routes ----------
@router.get("", response_model=PaginatedProducts)
def list_products(
    db: Session = Depends(get_db),
    _: CurrentUser = Depends(require_roles("admin", "staff")),
    q: Optional[str] = Query(default=None, description="Search by name/code/hsn_sac"),
    sort: Literal["created_at", "-created_at", "name", "-name", "price", "-price"] = "name",
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    stmt = select(Product)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(
            func.lower(Product.name).like(pattern)
            | func.lower(Product.code).like(pattern)
            | func.lower(Product.hsn_sac).like(pattern)
        )
    if sort in ("created_at", "name", "price"):
        stmt = stmt.order_by(getattr(Product, sort).asc())
    elif sort in ("-created_at", "-name", "-price"):
        stmt = stmt.order_by(getattr(Product, sort[1:]).desc())

    total = db.scalar(select(func.count()).select_from(stmt.subquery()))
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return PaginatedProducts(total=total or 0, items=items)

@router.post("", response_model=ProductOut, status_code=201)
def create_product(payload: ProductIn, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    ensure_unique_product(db, payload.name, payload.code)
    p = Product(
        name=payload.name,
        code=payload.code,
        hsn_sac=payload.hsn_sac,
        price=payload.price,
        tax_rate=payload.tax_rate,
        discount=payload.discount,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    return p

@router.put("/{product_id}", response_model=ProductOut)
def update_product(product_id: int, payload: ProductIn, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin", "staff"))):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    ensure_unique_product(db, payload.name, payload.code, exclude_id=product_id)

    p.name = payload.name
    p.code = payload.code
    p.hsn_sac = payload.hsn_sac
    p.price = payload.price
    p.tax_rate = payload.tax_rate
    p.discount = payload.discount
    p.updated_at = datetime.utcnow()

    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), _: CurrentUser = Depends(require_roles("admin"))):
    p = db.get(Product, product_id)
    if not p:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(p)
    db.commit()
    return
