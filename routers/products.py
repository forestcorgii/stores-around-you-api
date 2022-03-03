from fastapi import APIRouter,Depends
from sqlalchemy.orm import Session

from database import crud, models, schemas

from database.database import SessionLocal, engine
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from dependencies import get_token_header
router = APIRouter(
    prefix="/products",
    tags=["products"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
 

@router.get("/", response_model=list[schemas.Product])
def read_product(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    products = crud.get_products(db, skip=skip, limit=limit)
    return products

@router.post("/{store_id}/", response_model=schemas.Product)
def create_product_for_store(
    store_id: int, product: schemas.ProductCreate, db: Session = Depends(get_db)
):
    return crud.create_store_product(db=db, product=product, store_id=store_id)

