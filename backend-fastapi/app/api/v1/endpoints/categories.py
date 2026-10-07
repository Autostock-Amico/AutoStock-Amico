from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from app.core.database import db
from app.api.deps import get_current_user

router = APIRouter()

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = ""

class CategoryResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = ""

@router.get("", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_categories(current_user: dict = Depends(get_current_user)):
    cursor = db.categories.find().sort("createdAt", -1)
    categories = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        categories.append(doc)
    return categories

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreate,
    current_user: dict = Depends(get_current_user)
):
    name_clean = payload.name.strip()
    existing = await db.categories.find_one({"name": name_clean})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe una categoría con este nombre"
        )
    doc = {
        "name": name_clean,
        "description": payload.description.strip() if payload.description else ""
    }
    result = await db.categories.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc
