# services/product_service.py
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
import logging

from models.product import Product

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def get_product(db: Session, product_id: int) -> Optional[Product]:
    return db.get(Product, product_id)

def get_product_by_name(db: Session, name: str) -> Optional[Product]:
    if not name:
        return None
    return db.query(Product).filter(func.lower(Product.name) == name.lower()).one_or_none()

def create_product(db: Session, name: str, price: float, description: str | None = None, code: str | None = None, hsn_sac: str | None = None, tax_rate: float = 0.0, discount: float = 0.0, stock_quantity: int = 0) -> Product:
    if get_product_by_name(db, name):
        raise ServiceError("Product with same name already exists")
    p = Product(
        name=name,
        description=description,
        price=float(price),
        stock_quantity=int(stock_quantity),
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    # optional fields assignment if your Product model includes them
    if hasattr(p, "code") and code:
        p.code = code
    if hasattr(p, "hsn_sac") and hsn_sac:
        p.hsn_sac = hsn_sac
    if hasattr(p, "tax_rate"):
        p.tax_rate = float(tax_rate)
    if hasattr(p, "discount"):
        p.discount = float(discount)
    db.add(p)
    db.commit()
    db.refresh(p)
    logger.info("Created product %s (id=%s)", name, p.id)
    return p

def update_product(db: Session, product_id: int, *, name: str | None = None, price: float | None = None, description: str | None = None, stock_delta: int | None = None, **kwargs) -> Product:
    p = get_product(db, product_id)
    if not p:
        raise ServiceError("Product not found")
    if name is not None:
        # check uniqueness
        existing = get_product_by_name(db, name)
        if existing and existing.id != product_id:
            raise ServiceError("Another product with this name exists")
        p.name = name
    if price is not None:
        p.price = float(price)
    if description is not None:
        p.description = description
    if stock_delta is not None:
        # increment/decrement stock safely
        p.stock_quantity = max(0, int(p.stock_quantity or 0) + int(stock_delta))
    # optional fields
    if "tax_rate" in kwargs and hasattr(p, "tax_rate"):
        p.tax_rate = float(kwargs["tax_rate"])
    if "discount" in kwargs and hasattr(p, "discount"):
        p.discount = float(kwargs["discount"])
    p.updated_at = datetime.utcnow()
    db.add(p)
    db.commit()
    db.refresh(p)
    logger.info("Updated product id=%s", p.id)
    return p

def delete_product(db: Session, product_id: int) -> None:
    p = get_product(db, product_id)
    if not p:
        raise ServiceError("Product not found")
    db.delete(p)
    db.commit()
    logger.info("Deleted product id=%s", product_id)

def list_products(db: Session, q: str | None = None, page: int = 1, page_size: int = 25) -> dict:
    stmt = select(Product)
    if q:
        pattern = f"%{q.lower()}%"
        stmt = stmt.where(func.lower(Product.name).like(pattern) | func.lower(Product.description).like(pattern))
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return {"total": total, "items": items}
