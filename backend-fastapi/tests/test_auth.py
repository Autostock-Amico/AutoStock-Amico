USER = {"username": "santi", "email": "Santi@Test.com", "password": "santi123"}


def test_register_crea_usuario_sin_devolver_password(client):
    response = client.post("/api/auth/register", json=USER)
    assert response.status_code == 201
    body = response.json()
    assert body["username"] == "santi"
    assert body["email"] == "santi@test.com"
    assert "password" not in body


def test_register_rechaza_usuario_duplicado(client):
    client.post("/api/auth/register", json=USER)
    response = client.post("/api/auth/register", json={**USER, "email": "otro@test.com"})
    assert response.status_code == 400
    assert response.json()["detail"] == "El username o email ya está en uso"


def test_register_valida_email(client):
    response = client.post("/api/auth/register", json={**USER, "email": "no-es-email"})
    assert response.status_code == 422


def test_password_se_guarda_con_argon2(client):
    import app.api.v1.endpoints.auth as auth_module
    import asyncio

    client.post("/api/auth/register", json=USER)
    user = asyncio.run(auth_module.db.users.find_one({"username": "santi"}))
    assert user["password"].startswith("$argon2id$")


def test_login_con_username_y_con_email(client):
    client.post("/api/auth/register", json=USER)
    for identifier in ["santi", "SANTI@test.com"]:
        response = client.post("/api/auth/login", json={"identifier": identifier, "password": "santi123"})
        assert response.status_code == 200
        assert response.json()["token"]


def test_login_acepta_campo_username(client):
    client.post("/api/auth/register", json=USER)
    response = client.post("/api/auth/login", json={"username": "santi", "password": "santi123"})
    assert response.status_code == 200


def test_login_password_incorrecta(client):
    client.post("/api/auth/register", json=USER)
    response = client.post("/api/auth/login", json={"identifier": "santi", "password": "mal"})
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales inválidas"


def test_login_usuario_inexistente(client):
    response = client.post("/api/auth/login", json={"identifier": "nadie", "password": "x"})
    assert response.status_code == 401


def test_login_sin_identificador(client):
    response = client.post("/api/auth/login", json={"password": "x"})
    assert response.status_code == 400


def test_me_devuelve_datos_del_token(client, auth_headers):
    response = client.get("/api/auth/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["username"] == "santi"


def test_rutas_protegidas_sin_token(client):
    assert client.get("/api/products/").status_code in (401, 403)


def test_token_invalido(client):
    response = client.get("/api/products/", headers={"Authorization": "Bearer token-falso"})
    assert response.status_code == 401
