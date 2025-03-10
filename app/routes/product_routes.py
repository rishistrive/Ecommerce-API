from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.database import get_db
from app.logger import logger

router = APIRouter()


@router.post("/products/", response_model=schemas.Product)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(
        auth.get_current_user
    ),  # 🔐 Ensure user is authenticated
):
    """
    Create a new product in the database.

    Args:
        product (schemas.ProductCreate): Product data to create the product.
        db (Session): Database session injected via the `get_db` dependency.
        current_user (models.User): The currently authenticated user.

    Returns:
        schemas.Product: The newly created product.
    """
    logger.info(f"User {current_user.id} creating product: {product.name}")
    new_product = models.Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock=product.stock,
        user_id=current_user.id,  # 🔗 Link the product to the authenticated user
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info(f"Product {new_product.id} created successfully")
    return new_product


@router.get("/products/", response_model=list[schemas.Product])
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
    logger.info("Fetching products from database")
    products = crud.get_products(db=db, skip=skip, limit=limit)
    logger.info(f"Retrieved {len(products)} products")
    return products
