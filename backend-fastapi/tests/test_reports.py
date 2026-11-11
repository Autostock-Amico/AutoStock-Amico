import io

from openpyxl import load_workbook

from app.api.v1.endpoints.reports import inventory_metrics, is_critical


def test_reporte_excel_tiene_los_productos(client, product):
    response = client.get("/api/reports/excel")
    assert response.status_code == 200
    sheet = load_workbook(io.BytesIO(response.content)).active
    rows = list(sheet.values)
    assert rows[0][0] == "SKU"
    assert rows[1][0] == "FLT-001"
    assert rows[1][-1] == "CRÍTICO"


def test_reporte_pdf(client, product):
    response = client.get("/api/reports/pdf")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert response.content.startswith(b"%PDF")


def test_reporte_pdf_sin_productos_y_con_muchas_paginas(client, auth_headers):
    assert client.get("/api/reports/pdf").status_code == 200
    for i in range(60):
        client.post("/api/products/", json={
            "name": f"Producto {i}", "sku": f"PRD-{i:03d}", "category": "Varios",
            "costPrice": 1, "salePrice": 2, "currentStock": 10, "minStock": 1,
        }, headers=auth_headers)
    assert client.get("/api/reports/pdf").status_code == 200


def test_metricas_de_valorizacion():
    products = [
        {"costPrice": 10, "salePrice": 15, "currentStock": 2, "minStock": 5},
        {"costPrice": 5, "salePrice": 8, "currentStock": 10, "minStock": 1},
    ]
    metrics = inventory_metrics(products)
    assert metrics == {"total_items": 2, "total_units": 12, "cost_value": 70, "sale_value": 110}
    assert is_critical(products[0]) and not is_critical(products[1])
