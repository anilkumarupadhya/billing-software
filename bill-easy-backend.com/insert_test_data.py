from sqlalchemy import create_engine, Column, Integer, String, Float, MetaData, Table
from sqlalchemy.orm import sessionmaker

# MySQL connection using your env data
DATABASE_URL = "mysql+pymysql://odoo:Springodooca%2325@spring.cpkumva6xv1n.us-west-2.rds.amazonaws.com:3306/bill_easy_db"

engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define tables (minimal columns for testing)
customer = Table(
    'customer', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('email', String(255)),
    Column('phone', String(20)),
    Column('address', String(255))
)

product = Table(
    'product', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(255)),
    Column('price', Float),
    Column('sku', String(50)),
    Column('tax_rate', Float)
)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Insert test customer
session.execute(customer.insert().values(
    id=1,
    name="Test Customer",
    email="test@example.com",
    phone="1234567890",
    address="123 Test Street"
))

# Insert test product
session.execute(product.insert().values(
    id=1,
    name="Test Product",
    price=100,
    sku="TP001",
    tax_rate=0
))

session.commit()
session.close()
print("✅ Test customer and product inserted successfully.")

