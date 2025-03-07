from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    # Relationship to OrderItem
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product {self.name}>"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    status = Column(String, default="pending")

    # Relationship to OrderItem, which indirectly references Product
    order_items = relationship("OrderItem", back_populates="order")
    
    def __repr__(self):
        return f"<Order {self.id}>"

class OrderItem(Base):
    __tablename__ = "order_items"
    
    order_id = Column(Integer, ForeignKey('orders.id'), primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), primary_key=True)
    quantity = Column(Integer)

    # Relationship to the Order model
    order = relationship("Order", back_populates="order_items")
    
    # Relationship to the Product model
    product = relationship("Product", back_populates="order_items")
