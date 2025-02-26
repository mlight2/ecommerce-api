from pydantic import BaseModel, Field
from typing import List, Dict
from typing_extensions import Literal

class ProductBase(BaseModel):
    """Base schema for a product."""
    name: str
    description: str
    price: float
    stock: int

class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass

class Product(ProductBase):
    """Schema representing a product with an ID."""
    id: int

    class Config:
        orm_mode = True

class OrderItem(BaseModel):
    """Schema for an individual item in an order."""
    product_id: int
    quantity: int

class OrderBase(BaseModel):
    """Base schema for an order."""
    products: List[OrderItem]
    status: Literal["pending", "completed"] = "pending"

class OrderCreate(OrderBase):
    """Schema for creating an order (total_price removed)."""
    pass

class Order(OrderBase):
    """Schema representing an order with an ID and computed total price."""
    id: int
    total_price: float

    class Config:
        orm_mode = True
