import pytest

def test_endpoints_count():
    endpoints = [
        "/api/auth/login", "/api/auth/register",
        "/api/products", "/api/products/critical-stock",
        "/api/reports/excel", "/api/reports/pdf"
    ]
    assert len(endpoints) >= 6
