def test_product_critical_stock():
    stock = 2
    min_stock = 5
    assert stock <= min_stock

def test_product_structure():
    product = {"name": "Filtro de Aceite", "price": 4500.0, "stock": 10}
    assert product["price"] > 0
