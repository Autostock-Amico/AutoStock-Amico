from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from pymongo.errors import DuplicateKeyError

from app.api.deps import get_current_user
from app.core.database import db
from app.core.security import create_access_token, get_password_hash, verify_password
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

DUPLICATE_USER = "El username o email ya está en uso"
INVALID_CREDENTIALS = "Credenciales inválidas"


class LoginSchema(BaseModel):
    identifier: Optional[str] = Field(default=None, description="Username o Email")
    email: Optional[str] = None
    username: Optional[str] = None
    password: str

    def login_key(self) -> Optional[str]:
        return self.identifier or self.email or self.username


class TokenResponse(BaseModel):
    token: str


def find_by_username_or_email(username: str, email: str):
    return db.users.find_one({"$or": [{"username": username}, {"email": email}]})


@router.post("/register", response_model=UserResponse, status_code=201, response_model_by_alias=False)
async def register(datos: UserCreate):
    if await find_by_username_or_email(datos.username, datos.email):
        raise HTTPException(status_code=400, detail=DUPLICATE_USER)

    now = datetime.now(timezone.utc)
    documento = {
        "username": datos.username,
        "email": datos.email,
        "password": get_password_hash(datos.password),
        "createdAt": now,
        "updatedAt": now,
    }
    try:
        resultado = await db.users.insert_one(documento)
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail=DUPLICATE_USER)

    documento["_id"] = str(resultado.inserted_id)
    return documento


@router.post("/login", response_model=TokenResponse)
async def login(credentials: LoginSchema):
    login_key = credentials.login_key()
    if not login_key:
        raise HTTPException(status_code=400, detail="Se requiere un identificador (email o username) y contraseña")

    user = await find_by_username_or_email(login_key, login_key.lower())
    if not user or not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=INVALID_CREDENTIALS)

    return {"token": create_access_token(user)}


@router.get("/me")
async def get_me(current_user: dict = Depends(get_current_user)):
    return current_user
