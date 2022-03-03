
from fastapi import FastAPI,Depends

from dependencies import get_query_token
from routers import webhooks, products, stores
app = FastAPI(dependencies=[Depends(get_query_token)])
app.include_router(webhooks.router)
app.include_router(products.router)
app.include_router(stores.router)
