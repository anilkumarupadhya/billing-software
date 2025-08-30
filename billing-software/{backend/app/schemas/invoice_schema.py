# backend/app/schemas/invoice_schema.py
from pydantic import BaseModel, Field, root_validator, validator
from typing import List, Optional
from decimal import Decimal
from datetime import datetime
from app.schemas.customer_schema import CustomerOut  # for nested output
from app.schemas.product_schema import ProductOut

class InvoiceItemBase(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)
    price: Decimal = Field(..., gt=0)  # snapshot of product price

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}

class InvoiceItemCreate(InvoiceItemBase):
    pass

class InvoiceItemOut(InvoiceItemBase):
    id: int
    product: Optional[ProductOut] = None  # optional populated product info

    class Config:
        orm_mode = True

class InvoiceBase(BaseModel):
    customer_id: int = Field(..., gt=0)
    issued_date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = Field("pending", max_length=20)  # pending, paid, cancelled

class InvoiceCreate(InvoiceBase):
    items: List[InvoiceItemCreate] = Field(..., min_items=1)
    total_amount: Optional[Decimal] = Field(None, gt=0)

    @root_validator(pre=True)
    def ensure_total_or_compute(cls, values):
        """
        If total_amount not provided, compute from items.
        If provided, validate against items sum allowing small rounding differences.
        """
        items = values.get("items") or []
        # compute sum
        total = Decimal("0")
        for it in items:
            # it may be dict or object
            qty = Decimal(it.get("quantity")) if isinstance(it, dict) else Decimal(it.quantity)
            price = Decimal(str(it.get("price"))) if isinstance(it, dict) else Decimal(str(it.price))
            total += qty * price
        if values.get("total_amount") is None:
            values["total_amount"] = total
        else:
            provided = Decimal(str(values["total_amount"]))
            # allow small float rounding tolerance
            if abs(provided - total) > Decimal("0.01"):
                raise ValueError(f"total_amount ({provided}) does not match sum(items) ({total})")
        return values

    class Config:
        json_encoders = {Decimal: lambda v: float(v)}

class InvoiceUpdate(BaseModel):
    status: Optional[str] = Field(None, max_length=20)
    due_date: Optional[datetime] = None

class InvoiceOut(InvoiceBase):
    id: int
    total_amount: Decimal
    items: List[InvoiceItemOut]
    customer: Optional[CustomerOut] = None
    issued_date: datetime

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}
        schema_extra = {
            "example": {
                "id": 123,
                "customer": {
                    "id": 1,
                    "name": "Acme Corp",
                    "email": "billing@acme.example",
                    "phone": "+1-555-0100",
                    "address": "123 Main St"
                },
                "total_amount": 149.97,
                "status": "pending",
                "issued_date": "2025-08-27T10:00:00Z",
                "due_date": "2025-09-10T00:00:00Z",
                "items": [
                    {
                        "id": 1,
                        "product": {
                            "id": 10,
                            "name": "Widget A",
                            "description": "Standard widget",
                            "sku": "WIDGET-A-001",
                            "price": 49.99
                        },
                        "product_id": 10,
                        "quantity": 3,
                        "price": 49.99
                    }
                ]
            }
        }
