from pydantic import BaseModel
from typing import List

class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    
    class Config:
        from_attributes = True 

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    
    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    products: List[OrderItemBase]

class OrderResponse(BaseModel):
    id: int
    total_price: float
    status: str

    class Config:
        orm_mode = True
