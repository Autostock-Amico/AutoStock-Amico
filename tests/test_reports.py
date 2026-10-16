import pytest

def test_excel_header_format():
    headers = ["Nombre", "Categoría", "Precio", "Stock Actual", "Stock Mínimo"]
    assert len(headers) == 5
    assert "Stock Actual" in headers

def test_pdf_metadata():
    report_title = "Reporte de Resumen de Inventario"
    assert "Inventario" in report_title
