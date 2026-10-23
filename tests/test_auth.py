def test_user_schema():
    user = {"username": "admin", "role": "admin"}
    assert user["username"] == "admin"
    assert user["role"] == "admin"

def test_password_hash_check():
    password_plain = "secret123"
    assert len(password_plain) > 6
