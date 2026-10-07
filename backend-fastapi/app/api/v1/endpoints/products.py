from fastapi import APIRouter, HTTPException, status, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from bson import ObjectId
from app.core.database import db
from app.api.deps import get_current_user

router = APIRouter()

class StockUpdate(BaseModel):
    quantity: int = Field(..., gt=0, description="Cantidad a modificar")
    type: Literal["ENTRY", "EXIT", "add", "subtract"]

def serialize_product(doc):
    return {
        "id": str(doc["_id"]),
        "name": doc.get("name"),
        "sku": doc.get("sku"),
        "category": doc.get("category"),
        "costPrice": doc.get("costPrice"),
        "salePrice": doc.get("salePrice"),
        "currentStock": doc.get("currentStock", 0),
        "minStock": doc.get("minStock", 0),
        "createdAt": doc.get("createdAt"),
        "updatedAt": doc.get("updatedAt")
    }

@router.get("/")
async def get_products(
    search: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    current_user: dict = Depends(get_current_user)
):
    query = {}
    if search and search.strip():
        search_regex = {"$regex": search.strip(), "$options": "i"}
        query["$or"] = [{"name": search_regex}, {"sku": search_regex}]
    if category and category.strip():
        query["category"] = category.strip()

    cursor = db.products.find(query).sort("createdAt", -1)
    products = await cursor.to_list(length=100)
    return [serialize_product(p) for p in products]

@router.patch("/{product_id}/stock")
async def update_stock(
    product_id: str,
    payload: StockUpdate,
    current_user: dict = Depends(get_current_user)
):
    if not ObjectId.is_valid(product_id):
        raise HTTPException(status_code=400, detail="ID de producto inválido")

    obj_id = ObjectId(product_id)
    type_upper = payload.type.upper()
    is_entry = type_upper in ["ENTRY", "ADD"]
    adjustment = payload.quantity if is_entry else -payload.quantity

    filter_query = {"_id": obj_id}
    if not is_entry:
        filter_query["currentStock"] = {"$gte": payload.quantity}

    updated_doc = await db.products.find_one_and_update(
        filter_query,
        {"$inc": {"currentStock": adjustment}},
        return_document=True
    )

    if not updated_doc:
        exists = await db.products.find_one({"_id": obj_id})
        if not exists:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        raise HTTPException(status_code=400, detail="Stock insuficiente para realizar la operación")

    return serialize_product(updated_doc)
