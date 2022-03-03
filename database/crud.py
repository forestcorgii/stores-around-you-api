from sqlalchemy.orm import Session

from database import models, schemas


def get_store(db: Session, store_id: int):
    return db.query(models.Store).filter(models.Store.id == store_id).first()

def get_store_by_email(db: Session, email: str):
    return db.query(models.Store).filter(models.Store.email == email).first()

def get_stores(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Store).offset(skip).limit(limit).all()

def create_store(db: Session, store: schemas.StoreCreate):
    fake_hashed_password = store.password + "notreallyhashed"
    db_store = models.Store(email=store.email, hashed_password=fake_hashed_password)
    db.add(db_store)
    db.commit()
    db.refresh(db_store)
    return db_store

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()


def create_store_product(db: Session, product: schemas.ProductCreate, store_id: int):
    db_product = models.Product(**product.dict(), owner_id=store_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product



