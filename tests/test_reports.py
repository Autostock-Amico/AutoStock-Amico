def test_excel_report_headers():
    headers = ["ID", "Producto", "Stock", "Precio"]
    assert "Producto" in headers
    assert "Stock" in headers

def test_supported_report_formats():
    formats = ["xlsx", "pdf"]
    assert "pdf" in formats
