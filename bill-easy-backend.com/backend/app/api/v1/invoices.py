# app/api/v1/invoices.py
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging

# Import models directly from invoice.py to avoid circular imports
from app.models.invoice import Invoice, InvoiceItem
from app.models.customer import Customer
from app.models.product import Product

from app.core.config import get_db
from app.schemas import InvoiceCreate, InvoiceOut

router = APIRouter(prefix="/invoices", tags=["Invoices"])
logger = logging.getLogger(__name__)

# ------------------------------
# CREATE INVOICE
# ------------------------------
@router.post("/", response_model=InvoiceOut)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """
    Create a new invoice for testing without authentication.
    """
    customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
    if not customer:
        logger.error("Customer not found")
        raise HTTPException(status_code=404, detail="Customer not found")

    # Calculate total amount from items
    total_amount = 0
    for item in invoice.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        item_total = (product.price * item.quantity) - (item.discount or 0.0)
        total_amount += item_total

    # Create invoice with total_amount
    db_invoice = Invoice(
        customer_id=invoice.customer_id,
        total_amount=total_amount,
        status="pending"  # default status
    )
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    # Add invoice items
    for item in invoice.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        db_item = InvoiceItem(
            invoice_id=db_invoice.id,
            product_id=product.id,
            quantity=item.quantity,
            price=product.price,
            tax_rate=product.tax_rate,
            discount=item.discount or 0.0
        )
        db.add(db_item)

    db.commit()
    db.refresh(db_invoice)

    logger.info(f"Invoice {db_invoice.id} created successfully")
    return db_invoice

# ------------------------------
# GET INVOICE BY ID
# ------------------------------
@router.get("/{invoice_id}", response_model=InvoiceOut)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

# ------------------------------
# LIST INVOICES
# ------------------------------
@router.get("/", response_model=List[InvoiceOut])
def list_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(Invoice).offset(skip).limit(limit).all()

