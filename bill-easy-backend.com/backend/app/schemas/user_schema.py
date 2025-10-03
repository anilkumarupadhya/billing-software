# backend/app/schemas/user_schema.py
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=256)

    @validator("password")
    def password_strength(cls, v: str) -> str:
        # basic check; replace with stronger policy if desired
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None

class UserOut(UserBase):
    id: int
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 5,
                "email": "alice@example.com",
                "full_name": "Alice Example",
                "is_active": True,
                "is_superuser": False,
                "created_at": "2025-01-10T12:00:00Z"
            }
        }
