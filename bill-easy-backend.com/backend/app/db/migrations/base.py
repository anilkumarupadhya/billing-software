# db/base.py
from ..models.user import User
from ..models.customer import Customer
from ..models.product import Product
from ..models.invoice import Invoice
from ..models.payment import Payment

# Import all models here so Alembic (migrations) can detect them
__all__ = ["User", "Customer", "Product", "Invoice", "Payment"]
