# backend/app/schemas/customer_schema.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class CustomerBase(BaseModel):
    name: str = Field(..., max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class CustomerUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=15)
    address: Optional[str] = None


class CustomerOut(CustomerBase):
    id: int

    class Config:
        orm_mode = True

