from sqlalchemy import Column, Integer, String, Float, DateTime, func
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    tax_rate = Column(Float, default=0.0)  # <--- added tax_rate column

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

