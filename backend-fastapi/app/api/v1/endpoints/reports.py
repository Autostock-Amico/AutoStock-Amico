import io

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from app.core.database import db

router = APIRouter()

EXCEL_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
EXCEL_HEADERS = ["SKU", "Nombre", "Categoría", "Precio Costo", "Precio Venta", "Stock Actual", "Stock Mínimo", "Estado"]


def is_critical(product: dict) -> bool:
    return product.get("currentStock", 0) <= product.get("minStock", 0)


def product_row(product: dict) -> list:
    return [
        product.get("sku", ""),
        product.get("name", ""),
        product.get("category", ""),
        float(product.get("costPrice", 0)),
        float(product.get("salePrice", 0)),
        int(product.get("currentStock", 0)),
        int(product.get("minStock", 0)),
        "CRÍTICO" if is_critical(product) else "OK",
    ]


def inventory_metrics(products: list) -> dict:
    return {
        "total_items": len(products),
        "total_units": sum(int(p.get("currentStock", 0)) for p in products),
        "cost_value": sum(float(p.get("costPrice", 0)) * int(p.get("currentStock", 0)) for p in products),
        "sale_value": sum(float(p.get("salePrice", 0)) * int(p.get("currentStock", 0)) for p in products),
    }


def file_response(stream: io.BytesIO, media_type: str, filename: str) -> StreamingResponse:
    stream.seek(0)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(stream, media_type=media_type, headers=headers)


async def load_products() -> list:
    return await db.products.find().sort("name", 1).to_list(length=1000)


@router.get("/excel")
async def get_excel_report():
    products = await load_products()

    wb = Workbook()
    ws = wb.active
    ws.title = "Inventario"
    ws.append(EXCEL_HEADERS)
    for product in products:
        ws.append(product_row(product))

    stream = io.BytesIO()
    wb.save(stream)
    return file_response(stream, EXCEL_MEDIA_TYPE, "reporte_inventario.xlsx")


class PdfWriter:
    """Escribe líneas en el PDF y agrega páginas cuando se termina el espacio."""

    def __init__(self, stream: io.BytesIO):
        self.pdf = canvas.Canvas(stream, pagesize=letter)
        self.y = 750

    def line(self, text: str, font: str = "Helvetica", size: int = 10, gap: int = 15) -> None:
        if self.y < 50:
            self.pdf.showPage()
            self.y = 750
        self.pdf.setFont(font, size)
        self.pdf.drawString(50, self.y, text)
        self.y -= gap

    def save(self) -> None:
        self.pdf.save()


def write_summary(writer: PdfWriter, metrics: dict) -> None:
    writer.line("Reporte de Inventario - AutoStock", "Helvetica-Bold", 16, 30)
    writer.line(f"Total de productos: {metrics['total_items']}", size=12)
    writer.line(f"Unidades en stock: {metrics['total_units']}", size=12)
    writer.line(f"Valorización a costo: ${metrics['cost_value']:,.2f}", size=12)
    writer.line(f"Valorización a venta: ${metrics['sale_value']:,.2f}", size=12, gap=30)


def write_product_list(writer: PdfWriter, title: str, products: list) -> None:
    writer.line(title, "Helvetica-Bold", 12, 20)
    if not products:
        writer.line("Sin productos.")
    for p in products:
        writer.line(
            f"{p.get('sku', '')} | {p.get('name', '')} | Cat: {p.get('category', '')} | "
            f"Stock: {p.get('currentStock', 0)} (mín. {p.get('minStock', 0)}) | Venta: ${p.get('salePrice', 0)}"
        )
    writer.line("", gap=15)


@router.get("/pdf")
async def get_pdf_report():
    products = await load_products()

    stream = io.BytesIO()
    writer = PdfWriter(stream)
    write_summary(writer, inventory_metrics(products))
    write_product_list(writer, "Reposición urgente (stock crítico):", [p for p in products if is_critical(p)])
    write_product_list(writer, "Detalle de productos:", products)
    writer.save()

    return file_response(stream, "application/pdf", "reporte_inventario.pdf")
