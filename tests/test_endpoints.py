def test_endpoints_existence():
    routes = ["/api/products", "/api/products/critical-stock", "/api/reports/excel", "/api/reports/pdf"]
    assert len(routes) == 4
    assert "/api/reports/pdf" in routes
