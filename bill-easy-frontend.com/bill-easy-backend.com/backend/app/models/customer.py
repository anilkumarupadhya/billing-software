from sqlalchemy import Column, Integer, String, DateTime, func
from app.core.database import Base
from sqlalchemy.orm import relationship

class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    phone = Column(String(20), nullable=False)
    gst_no = Column(String(50), nullable=True)
    shipping_address = Column(String(500), nullable=False)
    billing_address = Column(String(500), nullable=False)
    eway = Column(String(100), nullable=True)
    # relationship to Invoice
    invoices = relationship("Invoice", back_populates="customer")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

