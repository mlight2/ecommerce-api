from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app import schemas, crud, database

router = APIRouter()

@router.post("/orders/", response_model=schemas.Order)
def create_order(order: schemas.OrderCreate, db: Session = Depends(database.get_db)):
    """
    Place a new order after validating stock availability.

    Args:
        order (schemas.OrderCreate): The order details including a list of product IDs and their quantities.
        db (Session): The database session dependency.

    Returns:
        schemas.Order: The successfully created order.

    Raises:
        HTTPException (400): If stock is insufficient for any product.
        HTTPException (404): If a product does not exist.
        HTTPException (500): If a database error occurs.
    """
    try:
        products_to_update = []
        for item in order.products:
            product = crud.get_product(db, item.product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"Product with ID {item.product_id} not found")
            if product.stock < item.quantity:
                raise HTTPException(status_code=400, detail=f"Insufficient stock for product {product.name}")
            products_to_update.append((product, item.quantity))

        for product, quantity in products_to_update:
            product.stock -= quantity
        db.commit()

        new_order = crud.create_order(db=db, order=order)
        return new_order

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error while processing order")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
