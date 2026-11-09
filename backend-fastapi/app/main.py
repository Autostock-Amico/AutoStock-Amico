from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints.auth import router as auth_router
from app.api.v1.endpoints.categories import router as categories_router
from app.api.v1.endpoints.products import router as products_router
from app.api.v1.endpoints.reports import router as reports_router

app = FastAPI(title="AutoStock API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(categories_router, prefix="/api/categories", tags=["categories"])
app.include_router(products_router, prefix="/api/products", tags=["products"])
app.include_router(reports_router, prefix="/api/reports", tags=["reports"])


@app.get("/")
def read_root():
    return {"message": "Backend FastAPI AutoStock corriendo perfectamente"}
