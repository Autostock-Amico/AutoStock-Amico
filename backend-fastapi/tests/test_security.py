import jwt

from app.core import security


def test_hash_y_verificacion_argon2():
    hashed = security.get_password_hash("secreta")
    assert hashed.startswith("$argon2id$")
    assert security.verify_password("secreta", hashed)
    assert not security.verify_password("otra", hashed)


def test_hash_que_no_es_argon2_no_valida():
    bcrypt_hash = "$2b$10$abcdefghijklmnopqrstuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuuu"
    assert security.verify_password("secreta", bcrypt_hash) is False


def test_token_contiene_datos_del_usuario():
    token = security.create_access_token({"_id": "abc123", "username": "santi", "email": "s@test.com"})
    payload = jwt.decode(token, security.SECRET_KEY, algorithms=[security.ALGORITHM])
    assert payload["sub"] == "abc123"
    assert payload["username"] == "santi"
    assert payload["exp"] > payload["iat"]
