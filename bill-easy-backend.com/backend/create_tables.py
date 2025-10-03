# create_tables.py
from app.core.database import Base, engine
from app.models.customer import Customer
from app.models.product import Product
from app.models.invoice import Invoice, InvoiceItem
from app.models.payment import Payment
from app.models.user import User

print("Creating tables in database...")

Base.metadata.create_all(bind=engine)

print("Tables created successfully!")

