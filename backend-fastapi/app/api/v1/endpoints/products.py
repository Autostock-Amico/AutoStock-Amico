from datetime import datetime, timezone
from typing import List, Optional
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.core.database import db
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse
from app.api.deps import get_current_user

router = APIRouter()

@router.get("", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK, include_in_schema=False)
async def get_products(
    search: Optional[str] = Query(default=None, description="Búsqueda parcial en nombre o SKU"),
    category: Optional[str] = Query(default=None, description="Filtro por categoría exacto"),
    current_user: dict = Depends(get_current_user)
):
    query = {}

    if search and search.strip():
        search_regex = {"$regex": search.strip(), "$options": "i"}
        query["$or"] = [
            {"name": search_regex},
            {"sku": search_regex}
        ]

    if category and category.strip():
        query["category"] = category.strip()

    cursor = db.products.find(query).sort("createdAt", -1)
    products = []
    async for doc in cursor:
        doc["id"] = str(doc["_id"])
        products.append(doc)
    return products

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    payload: ProductCreate,
    current_user: dict = Depends(get_current_user)
):
    sku_clean = payload.sku.strip()
    existing_sku = await db.products.find_one({"sku": sku_clean})
    if existing_sku:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un producto con este SKU"
        )

    ahora = datetime.now(timezone.utc)
    doc = {
        "name": payload.name.strip(),
        "sku": sku_clean,
        "category": payload.category.strip(),
        "costPrice": payload.costPrice,
        "salePrice": payload.salePrice,
        "currentStock": payload.currentStock,
        "minStock": payload.minStock,
        "createdAt": ahora,
        "updatedAt": ahora
    }

    result = await db.products.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return doc

@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(
    product_id: str,
    payload: ProductUpdate,
    current_user: dict = Depends(get_current_user)
):
    try:
        obj_id = ObjectId(product_id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de producto no válido"
        )

    existing = await db.products.find_one({"_id": obj_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items() if v is not None}

    if "sku" in update_data:
        sku_clean = update_data["sku"].strip()
        sku_duplicate = await db.products.find_one({"sku": sku_clean, "_id": {"$ne": obj_id}})
        if sku_duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El nuevo SKU ya está registrado en otro producto"
            )
        update_data["sku"] = sku_clean

    if "name" in update_data:
        update_data["name"] = update_data["name"].strip()
    if "category" in update_data:
        update_data["category"] = update_data["category"].strip()

    update_data["updatedAt"] = datetime.now(timezone.utc)

    await db.products.update_one({"_id": obj_id}, {"$set": update_data})
    updated_doc = await db.products.find_one({"_id": obj_id})
    updated_doc["id"] = str(updated_doc["_id"])
    return updated_doc

@router.delete("/{product_id}", status_code=status.HTTP_200_OK)
async def delete_product(
    product_id: str,
    current_user: dict = Depends(get_current_user)
):
    try:
        obj_id = ObjectId(product_id)
    except (InvalidId, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de producto no válido"
        )

    result = await db.products.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Producto no encontrado"
        )

    return {"message": "Producto eliminado exitosamente", "id": product_id}
