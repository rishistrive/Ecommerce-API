from sqlalchemy.orm import Session
from app.models import Product, Order, OrderItem
from app.schemas import ProductCreate, OrderCreate

# Create Product
def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

# Get all Products
def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

# Create Order
def create_order(db: Session, order: OrderCreate):
    total_price = 0.0
    order_items = []
    
    for item in order.products:
        if item.quantity <= 0:
            raise ValueError(f"Quantity for product {item.product_id} must be greater than zero.")
        
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if product and product.stock >= item.quantity:
            total_price += product.price * item.quantity
            product.stock -= item.quantity
            order_item = OrderItem(product_id=item.product_id, quantity=item.quantity)
            order_items.append(order_item)
        else:
            raise ValueError(f"Not enough stock for product {item.product_id}")

    db_order = Order(total_price=total_price)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    for order_item in order_items:
        order_item.order_id = db_order.id  # Make sure to set the order_id
        db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    
    return db_order
