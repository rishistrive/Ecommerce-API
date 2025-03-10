from typing import List

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class ProductBase(BaseModel):
    name: str = Field(
        ..., min_length=3, max_length=50, description="Product name (3-50 characters)"
    )
    description: str = Field(
        ...,
        min_length=5,
        max_length=500,
        description="Product description (5-500 characters)",
    )
    price: float = Field(
        ..., gt=0, description="Product price must be greater than zero"
    )
    stock: int = Field(..., ge=0, description="Stock quantity cannot be negative")

    class Config:
        from_attributes = True


class ProductCreate(ProductBase):
    pass


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str = Field(..., min_length=5)  # Minimum length requirement
    price: float
    stock: int


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
