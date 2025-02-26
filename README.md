# Ecommerce API

This is a FastAPI-based E-commerce API that allows you to manage products and orders efficiently.

## Features
- Create and retrieve products
- Place orders
- Handle stock management
- Built with FastAPI and SQLite

## Installation

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/ecommerce-api.git
cd ecommerce-api
```

### 2️⃣ Set Up a Virtual Environment
```sh
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```sh
pip install -r requirements.txt
```

### 4️⃣ Run the Application
```sh
uvicorn app.main:app --reload
```

## Running with Docker

### 1️⃣ Build the Docker Image
```sh
docker build -t ecommerce-api .
```

### 2️⃣ Run the Container
```sh
docker run -p 8000:8000 ecommerce-api
```

## Running Tests

### Run Tests Inside a Docker Container
```sh
docker build -t ecommerce-api-test .
docker run --rm ecommerce-api-test
```

### Run Tests Locally
```sh
python -m pytest -v
```

## API Endpoints & CURL Requests

### 1️⃣ Create a Product
```sh
curl -X POST "http://127.0.0.1:8000/products/" \
     -H "Content-Type: application/json" \
     -d '{"name": "Test Product", "description": "A test product", "price": 10.0, "stock": 100}'
```

### 2️⃣ Get All Products
```sh
curl -X GET "http://127.0.0.1:8000/products/"
```

### 3️⃣ Create an Order
```sh
curl -X POST "http://127.0.0.1:8000/orders/" \
     -H "Content-Type: application/json" \
     -d '{"products": [{"product_id": 1, "quantity": 2}]}'
```

## API Documentation
FastAPI provides interactive API documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Redoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

