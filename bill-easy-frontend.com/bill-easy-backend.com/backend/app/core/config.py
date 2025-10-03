# core/config.py
import os
from pydantic_settings import BaseSettings
from pydantic import Extra
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class Settings(BaseSettings):
    # Application
    APP_NAME: str = "BillEasy"
    APP_ENV: str = "production"  # development | staging | production
    APP_DEBUG: bool = False
    APP_PORT: int = 8000

    # Database
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Logging
    LOG_LEVEL: str = "info"

    # Frontend URL / CORS
    FRONTEND_URL: str

    class Config:
        env_file = ".env"
        extra = Extra.ignore

# Singleton instance
settings = Settings()

# SQLAlchemy engine & session
DATABASE_URL = f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for FastAPI
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

