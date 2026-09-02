import re
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator

EMAIL_REGEX = r"^\S+@\S+\.\S+$"


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @field_validator("username")
    @classmethod
    def username_no_vacio(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El username es obligatorio")
        return v.strip()

    @field_validator("email")
    @classmethod
    def email_formato_valido(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("El email es obligatorio")
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("El formato del email no es válido")
        return v.strip().lower()

    @field_validator("password")
    @classmethod
    def password_no_vacia(cls, v: str) -> str:
        if not v:
            raise ValueError("La password es obligatoria")
        return v


class UserResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(alias="_id")
    username: str
    email: str
    createdAt: Optional[datetime] = None
    updatedAt: Optional[datetime] = None

    @field_validator("id", mode="before")
    @classmethod
    def convertir_objectid_a_str(cls, v):
        return str(v)
