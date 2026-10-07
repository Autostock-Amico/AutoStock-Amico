from fastapi import FastAPI
from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.products import router as products_router

app = FastAPI()

app.include_router(auth_router, prefix="/api/auth")
app.include_router(categories_router, prefix="/api/categories")
app.include_router(products_router, prefix="/api/products")

@app.get("/")
async def root():
    return {"status": "ok"}
