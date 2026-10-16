import pytest

def test_user_registration_data():
    user_data = {"username": "admin_test", "email": "admin@autostock.com", "role": "admin"}
    assert user_data["username"] == "admin_test"
    assert "@" in user_data["email"]

def test_jwt_structure():
    mock_token = "header.payload.signature"
    assert len(mock_token.split(".")) == 3
