from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, description="Nombre único de la categoría")
    description: Optional[str] = Field(default="", description="Descripción opcional de la categoría")

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: str
    createdAt: datetime
    updatedAt: datetime
