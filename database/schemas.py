from pydantic import BaseModel


class ProductBase(BaseModel):
    name: str
    description: str = None
    type: str



class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class StoreBase(BaseModel):
    name: str
    description: str

class StoreCreate(StoreBase):
    password: str

class Store(StoreBase):
    id: int
    is_active: bool
    products: list[Product] = []

    class Config:
        orm_mode = True
