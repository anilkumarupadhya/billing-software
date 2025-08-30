from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.security import get_current_user
from core.config import get_db
from models import Invoice, InvoiceItem, Product, Customer
from schemas import InvoiceCreate, InvoiceResponse
from typing import List
import logging

router = APIRouter(prefix="/invoices", tags=["Invoices"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=InvoiceResponse)
def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Create a new invoice with customer, line items, and taxes applied.
    """
    customer = db.query(Customer).filter(Customer.id == invoice.customer_id).first()
    if not customer:
        logger.error("Customer not found")
        raise HTTPException(status_code=404, detail="Customer not found")

    db_invoice = Invoice(customer_id=invoice.customer_id, created_by=current_user["id"])
    db.add(db_invoice)
    db.commit()
    db.refresh(db_invoice)

    # Add invoice items
    for item in invoice.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")

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


@router.get("/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    Fetch a specific invoice by ID.
    """
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice


@router.get("/", response_model=List[InvoiceResponse])
def list_invoices(skip: int = 0, limit: int = 10, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    """
    List all invoices (paginated).
    """
    return db.query(Invoice).offset(skip).limit(limit).all()
