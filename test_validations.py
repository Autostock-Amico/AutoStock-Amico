from pydantic import ValidationError
from app.schemas.user import UserCreate

casos = [
    ("Caso correcto", {"username": "santino", "email": "santino@test.com", "password": "12345"}),
    ("Caso incorrecto 1 - falta username", {"email": "sinuser@test.com", "password": "12345"}),
    ("Caso incorrecto 2 - falta email", {"username": "sinemail", "password": "12345"}),
    ("Caso incorrecto 3 - email invalido", {"username": "emailmalo", "email": "esto-no-es-un-email", "password": "12345"}),
    ("Caso incorrecto 4 - password vacia", {"username": "sinpass", "email": "sinpass@test.com", "password": ""}),
]

for nombre, data in casos:
    try:
        user = UserCreate(**data)
        print(f"{nombre}: OK, se creo -> {user.username}")
    except ValidationError as e:
        print(f"{nombre}: ERROR (esperado) -> {e.errors()[0]['msg']}")
