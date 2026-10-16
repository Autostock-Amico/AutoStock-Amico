import pytest

def test_product_payload_validation():
    product = {"name": "Tornillo 1/2", "price": 150.0, "stock": 100, "minStock": 20}
    assert product["price"] > 0
    assert product["stock"] >= 0

def test_critical_stock_logic():
    stock = 5
    min_stock = 10
    is_critical = stock <= min_stock
    assert is_critical is True
