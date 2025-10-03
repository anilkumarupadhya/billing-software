from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_current_user
from core.config import get_db
from models import Payment, Invoice
from schemas import PaymentCreate, PaymentResponse
from typing import List
import logging

router = APIRouter(prefix="/payments", tags=["Payments"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=PaymentResponse)
def record_payment(payment: PaymentCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Record a payment against an invoice.
    """
    invoice = db.query(Invoice).filter(Invoice.id == payment.invoice_id).first()
    if not invoice:
        logger.error("Invoice not found for payment")
        raise HTTPException(status_code=404, detail="Invoice not found")

    db_payment = Payment(
        invoice_id=payment.invoice_id,
        amount=payment.amount,
        method=payment.method,
        reference=payment.reference
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    logger.info(f"Payment recorded for Invoice {invoice.id}")
    return db_payment


@router.get("/", response_model=List[PaymentResponse])
def list_payments(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    List all payments (paginated).
    """
    return db.query(Payment).offset(skip).limit(limit).all()
