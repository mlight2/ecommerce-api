from sqlalchemy import Column, Integer, String, Float, JSON
from app.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    products = Column(JSON)
    total_price = Column(Float)
    status = Column(String, default="pending")