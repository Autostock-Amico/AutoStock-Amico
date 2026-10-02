import os
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, ValidationError
from pymongo.errors import DuplicateKeyError

from app.core.database import db
from app.core.security import get_password_hash
from app.schemas.user import UserCreate, UserResponse
from app.api.deps import get_current_user

router = APIRouter()
ph = PasswordHasher()

SECRET_KEY = os.getenv("JWT_SECRET", "tu_clave_secreta_super_segura")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "480"))


class LoginSchema(BaseModel):
    identifier: str | None = Field(default=None, description="Username o Email")
    email: str | None = None
    username: str | None = None
    password: str


class TokenResponse(BaseModel):
    token: str


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
        documento["_id"] = str(resultado.inserted_id)
        return documento
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="El username o email ya esta en uso")


@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(credentials: LoginSchema):
    login_key = credentials.identifier or credentials.email or credentials.username

    if not login_key or not credentials.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Se requiere un identificador (email o username) y contraseña"
        )

    user = await db.users.find_one(
        {"$or": [{"username": login_key}, {"email": login_key}]}
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    try:
        ph.verify(user["password"], credentials.password)
    except (VerifyMismatchError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": str(user["_id"]),
        "email": user.get("email"),
        "username": user.get("username"),
        "iat": now,
        "exp": expire,
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"token": token}


@router.get("/me", status_code=status.HTTP_200_OK)
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
