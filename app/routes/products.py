from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import schemas, crud, database

router = APIRouter()

@router.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    """
    Create a new product in the database.

    Args:
        product (schemas.ProductCreate): The product details including name, description, price, and stock.
        db (Session): The database session dependency.

    Returns:
        schemas.Product: The created product.

    Raises:
        HTTPException (500): If a database error occurs.
    """
    try:
        return crud.create_product(db=db, product=product)
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while creating product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/products/", response_model=list[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    """
    Retrieve a list of products from the database.

    Args:
        skip (int, optional): The number of products to skip. Defaults to 0.
        limit (int, optional): The maximum number of products to return. Defaults to 100.
        db (Session): The database session dependency.

    Returns:
        list[schemas.Product]: A list of available products.

    Raises:
        HTTPException (500): If a database error occurs.
    """
    try:
        products = crud.get_products(db, skip=skip, limit=limit)
        return products
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving products")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: int, db: Session = Depends(database.get_db)):
    """
    Retrieve a single product by its ID.

    Args:
        product_id (int): The ID of the product to retrieve.
        db (Session): The database session dependency.

    Returns:
        schemas.Product: The requested product.

    Raises:
        HTTPException (404): If the product is not found.
        HTTPException (500): If a database error occurs.
    """
    try:
        product = crud.get_product(db, product_id=product_id)
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while retrieving product")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

