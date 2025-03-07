from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, crud, schemas, database
from app.database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    """
    Dependency to get a database session.

    This function creates a new database session for each request and ensures 
    that the session is properly closed when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Product routes
@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new product in the database.

    Args:
        product (schemas.ProductCreate): Product data to create the product.
        db (Session): Database session injected via the `get_db` dependency.

    Returns:
        schemas.Product: The newly created product.
    """
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def get_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of products from the database.

    Args:
        skip (int): Number of products to skip for pagination. Defaults to 0.
        limit (int): Maximum number of products to return. Defaults to 100.
        db (Session): Database session injected via the `get_db` dependency.

    Returns:
        list[schemas.Product]: List of products.
    """
    return crud.get_products(db=db, skip=skip, limit=limit)

# Order routes
@app.post("/orders/", response_model=schemas.OrderResponse)
def create_order(order: schemas.OrderCreate, db: Session = Depends(get_db)):
    """
    Create a new order in the database.

    Args:
        order (schemas.OrderCreate): Order data to create the order.
        db (Session): Database session injected via the `get_db` dependency.

    Returns:
        schemas.OrderResponse: The newly created order.
    
    Raises:
        HTTPException: If there's an issue with order creation (e.g., insufficient stock).
    """
    try:
        return crud.create_order(db=db, order=order)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orders/", response_model=list[schemas.OrderResponse])
def get_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of orders from the database.

    Args:
        skip (int): Number of orders to skip for pagination. Defaults to 0.
        limit (int): Maximum number of orders to return. Defaults to 100.
        db (Session): Database session injected via the `get_db` dependency.

    Returns:
        list[schemas.OrderResponse]: List of orders.
    """
    orders = db.query(models.Order).offset(skip).limit(limit).all()
    return orders

# Root endpoint
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint to check if the server is running.

    Returns:
        dict: A message confirming the server is running and providing 
              a link to the API documentation.
    """
    return {
        "message": "Server is running. Visit /docs for API documentation."
    }
