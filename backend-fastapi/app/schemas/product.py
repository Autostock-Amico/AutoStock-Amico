from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre del producto")
    sku: str = Field(..., min_length=1, description="Código SKU único")
    category: str = Field(..., min_length=1, description="ID o nombre de la categoría")
    costPrice: float = Field(..., ge=0, description="Precio de costo (>= 0)")
    salePrice: float = Field(..., ge=0, description="Precio de venta (>= 0)")
    currentStock: int = Field(default=0, ge=0, description="Stock actual (>= 0)")
    minStock: int = Field(default=0, ge=0, description="Stock mínimo (>= 0)")

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1)
    sku: Optional[str] = Field(default=None, min_length=1)
    category: Optional[str] = Field(default=None, min_length=1)
    costPrice: Optional[float] = Field(default=None, ge=0)
    salePrice: Optional[float] = Field(default=None, ge=0)
    currentStock: Optional[int] = Field(default=None, ge=0)
    minStock: Optional[int] = Field(default=None, ge=0)

class ProductResponse(BaseModel):
    id: str
    name: str
    sku: str
    category: str
    costPrice: float
    salePrice: float
    currentStock: int
    minStock: int
    createdAt: datetime
    updatedAt: datetime
