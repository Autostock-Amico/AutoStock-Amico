from tests.conftest import VALID_PRODUCT


def test_crear_producto_guarda_sku_en_mayusculas(product):
    assert product["sku"] == "FLT-001"
    assert product["id"]


def test_crear_producto_sku_duplicado(client, auth_headers, product):
    response = client.post("/api/products/", json=VALID_PRODUCT, headers=auth_headers)
    assert response.status_code == 400


def test_crear_producto_precio_negativo(client, auth_headers):
    response = client.post("/api/products/", json={**VALID_PRODUCT, "costPrice": -1}, headers=auth_headers)
    assert response.status_code == 422


def test_listar_y_filtrar_productos(client, auth_headers, product):
    assert len(client.get("/api/products/", headers=auth_headers).json()) == 1
    assert len(client.get("/api/products/?search=filtro", headers=auth_headers).json()) == 1
    assert len(client.get("/api/products/?search=(", headers=auth_headers).json()) == 0
    assert len(client.get("/api/products/?category=Filtros", headers=auth_headers).json()) == 1
    assert len(client.get("/api/products/?category=Otra", headers=auth_headers).json()) == 0


def test_stock_critico(client, auth_headers, product):
    critical = client.get("/api/products/critical-stock", headers=auth_headers).json()
    assert [p["sku"] for p in critical] == ["FLT-001"]


def test_editar_producto(client, auth_headers, product):
    response = client.put(f"/api/products/{product['id']}", json={"salePrice": 200, "sku": "flt-009"}, headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["salePrice"] == 200
    assert response.json()["sku"] == "FLT-009"


def test_editar_con_sku_de_otro_producto(client, auth_headers, product):
    client.post("/api/products/", json={**VALID_PRODUCT, "sku": "OTR-001"}, headers=auth_headers)
    response = client.put(f"/api/products/{product['id']}", json={"sku": "OTR-001"}, headers=auth_headers)
    assert response.status_code == 400


def test_editar_producto_inexistente_o_id_invalido(client, auth_headers):
    assert client.put("/api/products/64b000000000000000000000", json={"name": "x"}, headers=auth_headers).status_code == 404
    assert client.put("/api/products/abc", json={"name": "x"}, headers=auth_headers).status_code == 400


def test_entrada_y_salida_de_stock(client, auth_headers, product):
    url = f"/api/products/{product['id']}/stock"
    assert client.patch(url, json={"type": "IN", "quantity": 10}, headers=auth_headers).json()["currentStock"] == 12
    assert client.patch(url, json={"type": "OUT", "quantity": 2}, headers=auth_headers).json()["currentStock"] == 10


def test_salida_con_stock_insuficiente(client, auth_headers, product):
    response = client.patch(f"/api/products/{product['id']}/stock", json={"type": "OUT", "quantity": 50}, headers=auth_headers)
    assert response.status_code == 400
    assert "insuficiente" in response.json()["detail"]


def test_stock_producto_inexistente(client, auth_headers):
    response = client.patch("/api/products/64b000000000000000000000/stock", json={"type": "IN", "quantity": 1}, headers=auth_headers)
    assert response.status_code == 404


def test_stock_tipo_o_cantidad_invalidos(client, auth_headers, product):
    url = f"/api/products/{product['id']}/stock"
    assert client.patch(url, json={"type": "OTRO", "quantity": 1}, headers=auth_headers).status_code == 422
    assert client.patch(url, json={"type": "IN", "quantity": 0}, headers=auth_headers).status_code == 422


def test_eliminar_producto(client, auth_headers, product):
    assert client.delete(f"/api/products/{product['id']}", headers=auth_headers).status_code == 204
    assert client.delete(f"/api/products/{product['id']}", headers=auth_headers).status_code == 404
