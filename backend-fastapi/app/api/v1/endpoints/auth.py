from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException
from pydantic import ValidationError
from pymongo.errors import DuplicateKeyError

from app.core.database import db
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=201, response_model_by_alias=False)
async def register(payload: dict):
    try:
        datos = UserCreate(**payload)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=e.errors()[0]["msg"])

    existente = await db.users.find_one(
        {"$or": [{"username": datos.username}, {"email": datos.email}]}
    )
    if existente:
        raise HTTPException(status_code=400, detail="El username o email ya esta en uso")

    ahora = datetime.now(timezone.utc)
    documento = {
        "username": datos.username,
        "email": datos.email,
        "password": get_password_hash(datos.password),
        "createdAt": ahora,
        "updatedAt": ahora,
    }

    try:
        resultado = await db.users.insert_one(documento)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="El username o email ya esta en uso")

    documento["_id"] = resultado.inserted_id
    return UserResponse(**documento)
