from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    amount = Column(Float, nullable=False)
    method = Column(String(50))  # cash, card, UPI, bank transfer
    status = Column(String(20), default="completed")  # completed, failed, refunded
    payment_date = Column(DateTime(timezone=True), server_default=func.now())

    invoice = relationship("Invoice", backref="payments")
