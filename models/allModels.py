from pydantic import  BaseModel
from typing import *


# This currently contains the initial idea of models tat would be needed, can be later further segregated into other directory like Product, Order, User etc.

class Store(BaseModel):
    store_name: str
    creator: str

class UserCreate(BaseModel):
    user_name: str
    email: str
    user_type: str

class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    email: Optional[str] = None
    user_type: Optional[str] = None

class User(UserCreate, UserUpdate):
    user_id: str
    created_at: str
    updated_at: str


class ProductCreate(BaseModel):
    title: str
    description: str
    price: float
    image: str
    categories: list[str]
    tags: list[str]
    sizes: list[str]
    slug: str
    store_id: str

class ProductUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image: Optional[str] = None
    categories: Optional[list[str]] = None
    tags: Optional[list[str]] = None

class Product(ProductCreate, ProductUpdate):
    uid: int
    created_at: str
    updated_at: str

class Inventory(BaseModel):
    uid: int
    available_inventory: int
    store_id: str

class OrderItems(BaseModel):
    product_uid: int
    quantity: int

class Order(BaseModel):
    order_id: str
    user_id: str
    items: list[OrderItems]
    payment_mode: str
    created_at: Optional[str] = None
    status: str



