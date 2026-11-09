from datetime import datetime, timezone
from typing import Literal, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from pydantic import BaseModel, Field
from pymongo import ReturnDocument

from app.api.deps import get_current_user
from app.core.database import db
from app.schemas.product import ProductCreate, ProductUpdate

router = APIRouter()

ENTRY_TYPES = {"ENTRY", "ADD", "IN"}


class StockUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Cantidad a modificar")
    type: Literal["ENTRY", "EXIT", "IN", "OUT", "add", "subtract"]


def serialize_product(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "sku": doc.get("sku"),
        "category": doc.get("category"),
        "costPrice": doc.get("costPrice", 0),
        "salePrice": doc.get("salePrice", 0),
        "currentStock": doc.get("currentStock", 0),
        "minStock": doc.get("minStock", 0),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt"),
    }


def parse_object_id(product_id: str) -> ObjectId:
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")
    return ObjectId(product_id)


def build_search_query(search: Optional[str], category: Optional[str]) -> dict:
    query = {}
    if search and search.strip():
        search_regex = {"$regex": search.strip(), "$options": "i"}
        query["$or"] = [{"name": search_regex}, {"sku": search_regex}]
    if category and category.strip():
        query["category"] = category.strip()
    return query


async def ensure_unique_sku(sku: str, exclude_id: Optional[ObjectId] = None) -> None:
    query = {"sku": sku}
    if exclude_id is not None:
        query["_id"] = {"$ne": exclude_id}
    if await db.products.find_one(query):
        raise HTTPException(status_code=400, detail="Ya existe un producto con este SKU")


@router.get("/")
async def get_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user),
):
    cursor = db.products.find(build_search_query(search, category)).sort("createdAt", -1)
    products = await cursor.to_list(length=1000)
    return [serialize_product(p) for p in products]


# Debe ir ANTES de las rutas con {product_id}
@router.get("/critical-stock")
async def get_critical_stock(current_user: dict = Depends(get_current_user)):
    query = {"$expr": {"$lte": ["$currentStock", "$minStock"]}}
    products = await db.products.find(query).to_list(length=1000)
    return [serialize_product(p) for p in products]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, current_user: dict = Depends(get_current_user)):
    data = payload.model_dump()
    data["sku"] = data["sku"].strip().upper()
    await ensure_unique_sku(data["sku"])

    now = datetime.now(timezone.utc)
    data.update({"createdAt": now, "updatedAt": now})
    result = await db.products.insert_one(data)
    data["_id"] = result.inserted_id
    return serialize_product(data)


@router.put("/{product_id}")
async def update_product(
    product_id: str,
    payload: ProductUpdate,
    current_user: dict = Depends(get_current_user),
):
    obj_id = parse_object_id(product_id)
    changes = payload.model_dump(exclude_none=True)
    if "sku" in changes:
        changes["sku"] = changes["sku"].strip().upper()
        await ensure_unique_sku(changes["sku"], exclude_id=obj_id)

    changes["updatedAt"] = datetime.now(timezone.utc)
    updated = await db.products.find_one_and_update(
        {"_id": obj_id}, {"$set": changes}, return_document=ReturnDocument.AFTER
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return serialize_product(updated)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, current_user: dict = Depends(get_current_user)):
    result = await db.products.delete_one({"_id": parse_object_id(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.patch("/{product_id}/stock")
async def update_stock(
    product_id: str,
    payload: StockUpdate,
    current_user: dict = Depends(get_current_user),
):
    obj_id = parse_object_id(product_id)
    is_entry = payload.type.upper() in ENTRY_TYPES
    adjustment = payload.quantity if is_entry else -payload.quantity

    filter_query = {"_id": obj_id}
    if not is_entry:
        filter_query["currentStock"] = {"$gte": payload.quantity}

    updated = await db.products.find_one_and_update(
        filter_query,
        {"$inc": {"currentStock": adjustment}, "$set": {"updatedAt": datetime.now(timezone.utc)}},
        return_document=ReturnDocument.AFTER,
    )
    if updated:
        return serialize_product(updated)

    if not await db.products.find_one({"_id": obj_id}):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la operación")
