from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Future imports (uncomment once files exist)
# from app.api.v1 import users, customers, products, invoices, payments, reports

# Create FastAPI app instance
app = FastAPI(
    title="BillEasy - Billing Software API",
    description="Backend API for managing billing, invoicing, customers, and reports.",
    version="0.1.0"
)

# Enable CORS (important if frontend is React/Angular/Vue)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/", tags=["Health"])
def health_check():
    """
    Root endpoint to confirm the backend is running.
    """
    return {"status": "ok", "message": "BillEasy Backend is running 🚀"}

# Router includes (to be enabled when we add them)
# app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
# app.include_router(customers.router, prefix="/api/v1/customers", tags=["Customers"])
# app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])
# app.include_router(invoices.router, prefix="/api/v1/invoices", tags=["Invoices"])
# app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])
# app.include_router(reports.router, prefix="/api/v1/reports", tags=["Reports"])
