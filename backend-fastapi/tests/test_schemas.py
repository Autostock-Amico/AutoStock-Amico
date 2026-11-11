import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreate, UserResponse


def test_user_create_valido_normaliza_datos():
    user = UserCreate(username="  santino ", email="Santino@Test.com", password="12345")
    assert user.username == "santino"
    assert user.email == "santino@test.com"


@pytest.mark.parametrize("data", [
    {"username": " ", "email": "a@test.com", "password": "1"},
    {"username": "a", "email": " ", "password": "1"},
    {"username": "a", "email": "esto-no-es-un-email", "password": "1"},
    {"username": "a", "email": "a@test.com", "password": ""},
    {"email": "a@test.com", "password": "1"},
])
def test_user_create_invalido(data):
    with pytest.raises(ValidationError):
        UserCreate(**data)


def test_user_response_convierte_id_a_texto():
    from bson import ObjectId

    oid = ObjectId()
    response = UserResponse(_id=oid, username="a", email="a@test.com")
    assert response.id == str(oid)


def test_endpoint_raiz(client):
    assert client.get("/").status_code == 200
