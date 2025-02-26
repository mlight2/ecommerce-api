from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db, Base, engine
from sqlalchemy.orm import sessionmaker
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_ecommerce.db"
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# @pytest.fixture(scope="function")
# def db():
#     """Creates a fresh database session for each test."""
#     Base.metadata.create_all(bind=engine)
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#         Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """Create a database session without dropping tables."""
    db = TestingSessionLocal()
    transaction = db.begin()

    try:
        yield db
        transaction.rollback()
    finally:
        db.close()

client = TestClient(app)

def override_get_db():
    """Override FastAPI's database dependency with a test session."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db 

def test_create_product():
    """Test creating a new product."""
    response = client.post(
        "/products/",
        json={"name": "Test Product", "description": "A test product", "price": 10.0, "stock": 100}
    )
    print("get the respones ", response.json())
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"
    assert data["price"] == 10.0
    assert data["stock"] == 100

def test_get_products():
    """Test retrieving the product list."""
    client.post(
        "/products/",
        json={"name": "Sample Product", "description": "Sample description", "price": 15.5, "stock": 50}
    )
    
    response = client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_create_order_insufficient_stock():
    """Test placing an order when stock is insufficient."""
    product_response = client.post(
        "/products/",
        json={"name": "Low Stock Product", "description": "Limited stock", "price": 10.0, "stock": 1}
    )
    product_id = product_response.json()["id"]

    response = client.post(
        "/orders/",
        json={"products": [{"product_id": product_id, "quantity": 2}]}
    )
    assert response.status_code == 500
    assert "Insufficient stock" in response.json()["detail"]
