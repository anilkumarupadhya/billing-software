# backend/app/schemas/payment_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from decimal import Decimal

class PaymentBase(BaseModel):
    invoice_id: int = Field(..., gt=0)
    amount: Decimal = Field(..., gt=0)
    method: Optional[str] = Field(None, max_length=64)  # e.g., cash, card, upi, bank_transfer
    reference: Optional[str] = Field(None, max_length=255)  # txn ref / cheque no

class PaymentCreate(PaymentBase):
    paid_at: Optional[datetime] = None

class PaymentUpdate(BaseModel):
    amount: Optional[Decimal] = Field(None, gt=0)
    method: Optional[str] = Field(None, max_length=64)
    reference: Optional[str] = Field(None, max_length=255)

class PaymentOut(PaymentBase):
    id: int
    paid_at: Optional[datetime]

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}
        schema_extra = {
            "example": {
                "id": 101,
                "invoice_id": 55,
                "amount": 200.00,
                "method": "card",
                "reference": "TXN123456",
                "paid_at": "2025-08-27T10:15:00Z"
            }
        }
