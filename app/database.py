from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

DATABASE_URL = "sqlite:///./ecommerce.db"

try:
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    raise RuntimeError(f"Database connection failed: {str(e)}")

def get_db():
    """
    Dependency that provides a database session.
    
    Yields:
        db (Session): Database session object.

    Raises:
        HTTPException (500): If database session creation fails.
    """
    try:
        db = SessionLocal()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create database session: {str(e)}")
    
    try:
        yield db
    finally:
        try:
            db.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to close database session: {str(e)}")
