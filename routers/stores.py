from fastapi import APIRouter,Depends,HTTPException
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
    prefix="/stores",
    tags=["stores"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)
 

@router.post("/", response_model=schemas.Store)
def create_store(store: schemas.StoreCreate, db: Session = Depends(get_db)):
    db_store = crud.get_store_by_email(db, email=store.email)
    if db_store:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_store(db=db, store=store)


@router.get("/", response_model=list[schemas.Store])
def read_stores(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    stores = crud.get_stores(db, skip=skip, limit=limit)
    return stores


@router.get("/{store_id}", response_model=schemas.Store)
def read_user(store_id: int, db: Session = Depends(get_db)):
    db_store = crud.get_store(db, store_id=store_id)
    if db_store is None:
        raise HTTPException(status_code=404, detail="Store not found")
    return db_store
