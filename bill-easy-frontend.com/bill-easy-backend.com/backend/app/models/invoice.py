# app/models/invoice.py
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    total_amount = Column(Float, default=0.0)
    status = Column(String, default="pending")
    due_date = Column(DateTime)

    # Use string names in relationships to avoid circular imports
    customer = relationship("Customer", back_populates="invoices")
    items = relationship("InvoiceItem", back_populates="invoice")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
    price = Column(Float, default=0.0)
    tax_rate = Column(Float, default=0.0)
    discount = Column(Float, default=0.0)

    # Relationships
    invoice = relationship("Invoice", back_populates="items")
    product = relationship("Product")  # Use string "Product" if circular

