# insert_test_data.py
from app.core.database import SessionLocal
from app.models.customer import Customer
from app.models.product import Product

db = SessionLocal()

try:
    # Insert a test customer
    test_customer = Customer(
        name="Test Customer",
        email="test@example.com",
        phone="1234567890",
        address="123 Test Street"
    )
    db.add(test_customer)
    
    # Insert a test product
    test_product = Product(
        name="Test Product",
        price=100.0
    )
    db.add(test_product)

    db.commit()
    print("Test data inserted successfully!")
except Exception as e:
    db.rollback()
    print(f"Error: {e}")
finally:
    db.close()

