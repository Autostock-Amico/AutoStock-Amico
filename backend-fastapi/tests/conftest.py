"""Configuración común de los tests.

Los tests usan una base MongoDB simulada en memoria (mongomock-motor),
así que no necesitan Docker ni una base real para correr.
"""
import os

os.environ.setdefault("JWT_SECRET", "clave_de_test_con_mas_de_32_caracteres_ok")

import mongomock_motor  # noqa: E402
import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

import app.core.database as database  # noqa: E402
from app.api.v1.endpoints import auth, categories, products, reports  # noqa: E402
from app.main import app  # noqa: E402

MODULES_WITH_DB = [database, auth, categories, products, reports]

VALID_PRODUCT = {
    "name": "Filtro de Aceite",
    "sku": "flt-001",
    "category": "Filtros",
    "costPrice": 100,
    "salePrice": 150,
    "currentStock": 2,
    "minStock": 5,
}


@pytest.fixture
def client(monkeypatch):
    fake_db = mongomock_motor.AsyncMongoMockClient()["autostock_test"]
    for module in MODULES_WITH_DB:
        monkeypatch.setattr(module, "db", fake_db)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    client.post("/api/auth/register", json={"username": "santi", "email": "santi@test.com", "password": "santi123"})
    response = client.post("/api/auth/login", json={"identifier": "santi", "password": "santi123"})
    return {"Authorization": f"Bearer {response.json()['token']}"}


@pytest.fixture
def product(client, auth_headers):
    return client.post("/api/products/", json=VALID_PRODUCT, headers=auth_headers).json()
