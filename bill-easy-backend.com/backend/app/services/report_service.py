# services/report_service.py
from typing import Optional, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import select, func, and_
from datetime import datetime
import logging

from models.invoice import Invoice, InvoiceItem
from models.payment import Payment
from models.customer import Customer
from models.product import Product

logger = logging.getLogger(__name__)

class ServiceError(Exception):
    pass

def sales_summary(db: Session, date_from: Optional[datetime] = None, date_to: Optional[datetime] = None) -> Dict[str, Any]:
    """
    Returns totals: invoice_count, revenue, tax_collected, outstanding_amount
    """
    q = select(Invoice)
    if date_from:
        q = q.where(Invoice.issued_date >= date_from)
    if date_to:
        q = q.where(Invoice.issued_date <= date_to)

    # revenue and tax from invoice fields if present
    invoice_rows = db.execute(q).scalars().all()
    invoice_count = len(invoice_rows)
    revenue = 0.0
    tax_collected = 0.0
    outstanding = 0.0

    for inv in invoice_rows:
        inv_total = float(getattr(inv, "total_amount", getattr(inv, "total", 0.0) or 0.0))
        inv_tax = float(getattr(inv, "total_tax", 0.0) or 0.0)
        revenue += inv_total
        tax_collected += inv_tax
        if getattr(inv, "status", "").lower() not in ("paid", "completed"):
            outstanding += inv_total

    return {
        "invoice_count": invoice_count,
        "revenue": revenue,
        "tax_collected": tax_collected,
        "outstanding": outstanding,
    }

def outstanding_invoices(db: Session, limit: int = 100) -> List[Dict[str, Any]]:
    """
    Return list of outstanding invoices with customer and amounts.
    """
    q = select(Invoice).where(Invoice.status != "paid").order_by(Invoice.issued_date.asc()).limit(limit)
    rows = db.execute(q).scalars().all()
    out = []
    for inv in rows:
        customer = db.get(Customer, inv.customer_id)
        out.append({
            "invoice_id": inv.id,
            "invoice_number": getattr(inv, "number", None),
            "customer_id": inv.customer_id,
            "customer_name": getattr(customer, "name", None) if customer else None,
            "status": inv.status,
            "total": float(getattr(inv, "total_amount", getattr(inv, "total", 0.0) or 0.0))
        })
    return out

def top_customers_by_revenue(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Aggregate revenue per customer from invoices.
    """
    stmt = select(Invoice.customer_id, func.coalesce(func.sum(getattr(Invoice, "total_amount", getattr(Invoice, "total", 0.0))), 0.0).label("revenue")).group_by(Invoice.customer_id).order_by(func.sum(getattr(Invoice, "total_amount", getattr(Invoice, "total", 0.0))).desc()).limit(limit)
    rows = db.execute(stmt).all()
    out = []
    for cust_id, revenue in rows:
        cust = db.get(Customer, cust_id)
        out.append({"customer_id": cust_id, "customer_name": getattr(cust, "name", None) if cust else None, "revenue": float(revenue)})
    return out

def top_products_sold(db: Session, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Aggregate quantities sold per product from invoice items.
    """
    stmt = select(InvoiceItem.product_id, func.coalesce(func.sum(InvoiceItem.quantity), 0).label("qty")).group_by(InvoiceItem.product_id).order_by(func.sum(InvoiceItem.quantity).desc()).limit(limit)
    rows = db.execute(stmt).all()
    out = []
    for product_id, qty in rows:
        p = db.get(Product, product_id)
        out.append({"product_id": product_id, "product_name": getattr(p, "name", None) if p else None, "quantity_sold": int(qty)})
    return out
