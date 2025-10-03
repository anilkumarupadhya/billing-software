# services/payment_service.py
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from datetime import datetime
import logging

from models.payment import Payment
from models.invoice import Invoice
from models.invoice import InvoiceItem

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def record_payment(db: Session, invoice_id: int, amount: float, method: str, reference: str | None = None, paid_at: datetime | None = None) -> Payment:
    """
    Record a payment and update invoice status (partial/paid).
    """
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise ServiceError("Invoice not found")

    if float(amount) <= 0:
        raise ServiceError("Amount must be positive")

    payment = Payment(
        invoice_id=invoice_id,
        amount=float(amount),
        method=method,
        reference=reference,
        payment_date=paid_at or datetime.utcnow(),
        status="completed"
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # Recalculate total paid and update invoice status
    total_paid = db.query(func.coalesce(func.sum(Payment.amount), 0.0)).filter(Payment.invoice_id == invoice_id).scalar() or 0.0
    invoice_total = float(getattr(invoice, "total_amount", getattr(invoice, "total", 0.0) or 0.0))

    if total_paid >= invoice_total and invoice_total > 0:
        invoice.status = "paid"
    elif 0 < total_paid < invoice_total:
        invoice.status = "partial"
    else:
        invoice.status = "unpaid"

    invoice.updated_at = datetime.utcnow() if hasattr(invoice, "updated_at") else None
    db.add(invoice)
    db.commit()
    db.refresh(invoice)

    logger.info("Recorded payment %.2f for invoice id=%s (status=%s)", amount, invoice_id, invoice.status)
    return payment

def get_payment(db: Session, payment_id: int) -> Optional[Payment]:
    return db.get(Payment, payment_id)

def list_payments(db: Session, invoice_id: int | None = None, page: int = 1, page_size: int = 25) -> dict:
    stmt = select(Payment)
    if invoice_id:
        stmt = stmt.where(Payment.invoice_id == invoice_id)
    total = db.execute(select(func.count()).select_from(stmt.subquery())).scalar() or 0
    items = db.execute(stmt.offset((page - 1) * page_size).limit(page_size)).scalars().all()
    return {"total": total, "items": items}
