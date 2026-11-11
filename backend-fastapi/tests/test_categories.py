def test_crear_y_listar_categorias(client, auth_headers):
    response = client.post("/api/categories", json={"name": " Filtros ", "description": "Repuestos"}, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["name"] == "Filtros"

    names = [c["name"] for c in client.get("/api/categories", headers=auth_headers).json()]
    assert names == ["Filtros"]


def test_categoria_duplicada(client, auth_headers):
    client.post("/api/categories", json={"name": "Frenos"}, headers=auth_headers)
    response = client.post("/api/categories", json={"name": "Frenos"}, headers=auth_headers)
    assert response.status_code == 400
