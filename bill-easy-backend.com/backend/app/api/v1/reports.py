from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.security import get_current_user
from core.config import get_db
from models import Invoice, Payment
from typing import Dict
import logging

router = APIRouter(prefix="/reports", tags=["Reports"])
logger = logging.getLogger(__name__)


@router.get("/sales-summary")
def sales_summary(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> Dict:
    """
    Generate a sales summary report (total invoices & revenue).
    """
    total_invoices = db.query(Invoice).count()
    total_revenue = db.query(Invoice).with_entities(
        (Invoice.total).label("revenue")
    ).all()

    revenue_sum = sum(r.revenue for r in total_revenue if r.revenue)

    return {"total_invoices": total_invoices, "total_revenue": revenue_sum}


@router.get("/outstanding-payments")
def outstanding_payments(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> Dict:
    """
    Report of outstanding (unpaid) invoices.
    """
    outstanding = db.query(Invoice).filter(Invoice.status != "PAID").count()
    return {"outstanding_invoices": outstanding}


@router.get("/tax-report")
def tax_report(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)) -> Dict:
    """
    Tax report summary (total GST/VAT collected).
    """
    invoices = db.query(Invoice).all()
    total_tax = sum(inv.total_tax for inv in invoices if inv.total_tax)

    return {"total_tax_collected": total_tax}
