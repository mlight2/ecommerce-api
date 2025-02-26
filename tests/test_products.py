import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import get_db, Base, engine
from app import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ecommerce.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    """Creates a fresh test database session for each test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    app.dependency_overrides[get_db] = lambda: db  # Override FastAPI DB dependency
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)
        app.dependency_overrides.clear()  # Reset override

client = TestClient(app)

@pytest.fixture(scope="function")
def client_with_db(db):
    def override_get_db():
        yield db
    app.dependency_overrides[get_db] = override_get_db  # Override DB
    return TestClient(app)

def test_create_order(db):
    """Test creating an order when stock is available."""
    product = models.Product(name="Test Product", description="A test product", price=10.0, stock=100)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post("/orders/", json={"products": [{"product_id": product.id, "quantity": 2}]})

    assert response.status_code == 200
    assert response.json()["status"] == "pending"



def test_create_order_insufficient_stock(db):
    """Test placing an order when stock is insufficient."""
    product = models.Product(name="Low Stock Product", description="Limited stock", price=10.0, stock=1)
    db.add(product)
    db.commit()
    db.refresh(product)

    response = client.post("/orders/", json={"products": [{"product_id": product.id, "quantity": 2}]})
    assert "Insufficient stock" in response.json()["detail"]

def test_create_order_product_not_found(db):
    """Test ordering a non-existent product."""
    response = client.post("/orders/", json={"products": [{"product_id": 999, "quantity": 2}]})
    assert "Product with ID 999 not found" in response.json()["detail"]