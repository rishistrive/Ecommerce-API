from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")
    products = relationship("Product", back_populates="owner")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    order_items = relationship("OrderItem", back_populates="product")
    owner = relationship("User", back_populates="products")

    def __repr__(self):
        return f"<Product {self.name}>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_price = Column(Float)
    status = Column(String, default="pending")

    user = relationship("User", back_populates="orders")
    order_items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id}>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("products.id"), primary_key=True)
    quantity = Column(Integer)

    # Relationship to the Order model
    order = relationship("Order", back_populates="order_items")

    # Relationship to the Product model
    product = relationship("Product", back_populates="order_items")
