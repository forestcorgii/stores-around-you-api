from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database.database import Base

class Store(Base):
    __tablename__ = 'stores'

    id = Column(Integer, primary_key=True,index=True)
    hashed_password = Column(String)
    name = Column(String, index=True)
    description = Column(String)
    facebook_url = Column(String)
    image_url = Column(String)


    products = relationship("Product", back_populates="owner")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    type=Column(String,index=True)
    owner_id = Column(Integer, ForeignKey("stores.id"))
    image_url = Column(String)
    

    owner = relationship("Store", back_populates="products")
