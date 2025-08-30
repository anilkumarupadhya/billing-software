"""
Billing Software Backend Package

This package contains all backend code for the Billing Software.
It is structured into modules for users, customers, products, invoices,
payments, and reports.

Modules:
    - api: API routes (FastAPI routers grouped by feature)
    - core: Core settings and security logic
    - models: SQLAlchemy ORM models for database tables
    - services: Business logic for billing operations
    - utils: Helper utilities (email, pdf generation, etc.)
"""

# Expose package-level constants or shortcuts here if needed
__version__ = "0.1.0"
