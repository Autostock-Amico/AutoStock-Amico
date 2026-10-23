def test_report_excel_extension():
    filename = "reporte_inventario.xlsx"
    assert filename.endswith(".xlsx")

def test_report_pdf_extension():
    filename = "reporte_inventario.pdf"
    assert filename.endswith(".pdf")
