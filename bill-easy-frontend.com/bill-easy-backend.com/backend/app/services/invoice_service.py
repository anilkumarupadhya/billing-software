# services/invoice_service.py
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
import logging

from models.invoice import Invoice, InvoiceItem
from models.product import Product
from models.customer import Customer

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def _generate_invoice_number(db: Session) -> str:
    """
    Simple invoice numbering: YYYYMMDD-XXXX where XXXX is a daily sequence.
    """
    today = datetime.utcnow().date()
    prefix = today.strftime("%Y%m%d")
    # count invoices today
    q = select(func.count()).select_from(Invoice).where(func.date(Invoice.issued_date) == today)
    cnt = db.execute(q).scalar() or 0
    seq = cnt + 1
    return f"{prefix}-{seq:04d}"

def calculate_line_amount(product: Product, quantity: float, unit_price: float | None = None, discount_pct: float = 0.0) -> Dict[str, float]:
    """
    Return dict with subtotal, tax, total for a line item (no DB interaction).
    """
    price = float(unit_price if unit_price is not None else product.price)
    qty = float(quantity)
    subtotal = price * qty
    discount = subtotal * (float(discount_pct or 0.0) / 100.0)
    taxable = max(0.0, subtotal - discount)
    tax_rate = float(getattr(product, "tax_rate", 0.0) or 0.0)
    tax = taxable * (tax_rate / 100.0)
    total = taxable + tax
    return {"subtotal": subtotal, "discount": discount, "taxable": taxable, "tax": tax, "total": total}

def create_invoice(db: Session, customer_id: int, items: List[Dict[str, Any]], issue_date: Optional[datetime] = None, due_date: Optional[datetime] = None, notes: Optional[str] = None, created_by: Optional[int] = None) -> Invoice:
    """
    items: list of {product_id, quantity, unit_price (optional), discount_pct (optional)}
    Calculates totals, persists Invoice and InvoiceItems, updates product stock (if available).
    """
    customer = db.get(Customer, customer_id)
    if not customer:
        raise ServiceError("Customer not found")

    if not items or not isinstance(items, list):
        raise ServiceError("Invoice must have at least one item")

    invoice = Invoice(
        customer_id=customer_id,
        number=_generate_invoice_number(db),
        issued_date=issue_date or datetime.utcnow(),
        due_date=due_date,
        status="pending",
        notes=notes,
        created_at=datetime.utcnow() if hasattr(Invoice, "created_at") else None
    )
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    total_amount = 0.0
    total_tax = 0.0
    total_subtotal = 0.0

    for it in items:
        product_id = int(it["product_id"])
        quantity = float(it.get("quantity", 1.0))
        unit_price = it.get("unit_price")
        discount_pct = float(it.get("discount_pct", 0.0))

        product = db.get(Product, product_id)
        if not product:
            db.rollback()
            raise ServiceError(f"Product {product_id} not found")

        line = calculate_line_amount(product, quantity, unit_price, discount_pct)

        inv_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=product_id,
            quantity=quantity,
            price=float(unit_price if unit_price is not None else product.price),
            tax_rate=float(getattr(product, "tax_rate", 0.0) or 0.0),
            discount=float(discount_pct),
            subtotal=line["subtotal"],
            tax=line["tax"],
            total=line["total"],
        )
        # some InvoiceItem models might not have these fields; guard assignment in model
        db.add(inv_item)

        # update stock if model has stock_quantity
        if hasattr(product, "stock_quantity"):
            try:
                product.stock_quantity = max(0, int(product.stock_quantity or 0) - int(quantity))
                db.add(product)
            except Exception:
                # do not fail invoice creation for stock update errors, but log
                logger.exception("Failed to update stock for product %s", product_id)

        total_amount += line["total"]
        total_tax += line["tax"]
        total_subtotal += line["subtotal"]

    # commit items and product updates
    db.commit()
    # refresh invoice to pick up items if relationship exists
    db.refresh(invoice)

    # set computed totals on invoice if attributes exist
    if hasattr(invoice, "total_amount"):
        invoice.total_amount = float(total_amount)
    if hasattr(invoice, "total_tax"):
        invoice.total_tax = float(total_tax)
    if hasattr(invoice, "subtotal"):
        invoice.subtotal = float(total_subtotal)

    invoice.status = "unpaid" if total_amount > 0 else "paid"
    invoice.updated_at = datetime.utcnow() if hasattr(invoice, "updated_at") else None
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    logger.info("Created invoice %s (id=%s) customer=%s total=%.2f", invoice.number, invoice.id, customer_id, total_amount)
    return invoice

def get_invoice(db: Session, invoice_id: int) -> Optional[Invoice]:
    return db.get(Invoice, invoice_id)

def list_invoices(db: Session, page: int = 1, page_size: int = 25, q: str | None = None) -> dict:
    stmt = select(Invoice)
    if q:
        pattern = f"%{q.lower()}%"
        # basic search across invoice number
        stmt = stmt.where(func.lower(Invoice.number).like(pattern))
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return {"total": total, "items": items}
