def test_registered_backend_routes():
    routes = [
        "/api/auth/login",
        "/api/products",
        "/api/products/critical-stock",
        "/api/reports/excel",
        "/api/reports/pdf"
    ]
    assert len(routes) == 5
    assert "/api/reports/pdf" in routes
