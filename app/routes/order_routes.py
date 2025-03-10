from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import auth, models, schemas
from app.database import get_db
from app.logger import logger

router = APIRouter()


@router.post("/orders/", response_model=schemas.OrderResponse)
def create_order(
    order: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Create an order, ensuring the logged-in user is associated with it.
    """
    logger.info(f"User {current_user.id} placing an order")
    try:
        total_price = 0.0
        order_items = []

        for item in order.products:
            product = (
                db.query(models.Product)
                .filter(models.Product.id == item.product_id)
                .first()
            )
            if not product or product.stock < item.quantity:
                logger.warning(f"Not enough stock for product {item.product_id}")
                raise HTTPException(
                    status_code=400,
                    detail=f"Not enough stock for product {item.product_id}",
                )

            total_price += product.price * item.quantity
            order_items.append(
                models.OrderItem(product_id=item.product_id, quantity=item.quantity)
            )

        db_order = models.Order(
            user_id=current_user.id, total_price=total_price, status="pending"
        )
        db.add(db_order)
        db.commit()
        db.refresh(db_order)

        # Deduct stock
        for item in order.products:
            product = (
                db.query(models.Product)
                .filter(models.Product.id == item.product_id)
                .first()
            )
            product.stock -= item.quantity
            db.add(product)

        # Save order items
        for order_item in order_items:
            order_item.order_id = db_order.id
            db.add(order_item)

        db.commit()
        db.refresh(db_order)
        logger.info(f"Order {db_order.id} created successfully")
        return db_order
    except Exception as e:
        db.rollback()
        logger.error(f"Error creating order: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/orders/", response_model=list[schemas.OrderResponse])
def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user),
):
    """
    Retrieve a list of orders for the logged-in user.

    Args:
        skip (int): Number of orders to skip for pagination. Defaults to 0.
        limit (int): Maximum number of orders to return. Defaults to 100.
        db (Session): Database session injected via the `get_db` dependency.
        current_user (models.User): The currently authenticated user.

    Returns:
        list[schemas.OrderResponse]: List of the user's orders.
    """
    logger.info(f"Fetching orders for user {current_user.id}")
    orders = (
        db.query(models.Order)
        .filter(models.Order.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    logger.info(f"Retrieved {len(orders)} orders")
    return orders
