# backend/app/schemas/product_schema.py
from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2048)
    sku: Optional[str] = Field(None, max_length=128)
    price: Decimal = Field(..., gt=0)  # use Decimal for money

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2048)
    sku: Optional[str] = Field(None, max_length=128)
    price: Optional[Decimal] = Field(None, gt=0)

class ProductOut(ProductBase):
    id: int

    class Config:
        orm_mode = True
        json_encoders = {Decimal: lambda v: float(v)}
        schema_extra = {
            "example": {
                "id": 10,
                "name": "Widget A",
                "description": "Standard widget, 1 year warranty",
                "sku": "WIDGET-A-001",
                "price": 49.99
            }
        }
