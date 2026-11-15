import io
from datetime import datetime

from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from app.core.database import db

router = APIRouter()

EXCEL_MEDIA_TYPE = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
EXCEL_HEADERS = ["SKU", "Nombre", "Categoría", "Precio Costo", "Precio Venta", "Stock Actual", "Stock Mínimo", "Estado"]
EXCEL_WIDTHS = [14, 32, 18, 16, 16, 14, 14, 12]
MONEY_FORMAT = '"$" #,##0.00'

# Colores compartidos (mismos que el frontend)
GREEN = "16A34A"
RED = "DC2626"
RED_LIGHT = "FDE2E2"
GRAY_LIGHT = "F3F4F6"
DARK = "1E222B"


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


def money(value: float) -> str:
    """Formato argentino: $ 1.234,56"""
    return "$ " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def file_response(stream: io.BytesIO, media_type: str, filename: str) -> StreamingResponse:
    stream.seek(0)
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return StreamingResponse(stream, media_type=media_type, headers=headers)


async def load_products() -> list:
    return await db.products.find().sort("name", 1).to_list(length=1000)


# ===================== EXCEL =====================

def style_header(ws) -> None:
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=GREEN)
        cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 22
    for index, width in enumerate(EXCEL_WIDTHS, start=1):
        ws.column_dimensions[ws.cell(row=1, column=index).column_letter].width = width
    ws.freeze_panes = "A2"


def style_product_row(ws, row_number: int, critical: bool) -> None:
    border = Border(bottom=Side(style="thin", color="E5E7EB"))
    for cell in ws[row_number]:
        cell.border = border
        if critical:
            cell.fill = PatternFill("solid", fgColor=RED_LIGHT)
    for column in ("D", "E"):
        ws[f"{column}{row_number}"].number_format = MONEY_FORMAT
    status = ws[f"H{row_number}"]
    status.font = Font(bold=True, color=RED if critical else GREEN)
    status.alignment = Alignment(horizontal="center")


def write_inventory_sheet(ws, products: list) -> None:
    ws.title = "Inventario"
    ws.append(EXCEL_HEADERS)
    style_header(ws)
    for product in products:
        ws.append(product_row(product))
        style_product_row(ws, ws.max_row, is_critical(product))
    ws.auto_filter.ref = ws.dimensions


def write_summary_sheet(ws, products: list) -> None:
    metrics = inventory_metrics(products)
    rows = [
        ("Reporte de Inventario - AutoStock", None),
        ("Generado", datetime.now().strftime("%d/%m/%Y %H:%M")),
        ("Total de productos", metrics["total_items"]),
        ("Unidades en stock", metrics["total_units"]),
        ("Productos en stock crítico", sum(1 for p in products if is_critical(p))),
        ("Valorización a costo", metrics["cost_value"]),
        ("Valorización a venta", metrics["sale_value"]),
    ]
    for row in rows:
        ws.append(row)
    ws["A1"].font = Font(bold=True, size=14, color=GREEN)
    for cell in ("B6", "B7"):
        ws[cell].number_format = MONEY_FORMAT
    for row in ws.iter_rows(min_row=2, max_col=1):
        row[0].font = Font(bold=True)
    ws.column_dimensions["A"].width = 30
    ws.column_dimensions["B"].width = 22


@router.get("/excel")
async def get_excel_report():
    products = await load_products()

    wb = Workbook()
    write_inventory_sheet(wb.active, products)
    write_summary_sheet(wb.create_sheet("Resumen"), products)

    stream = io.BytesIO()
    wb.save(stream)
    return file_response(stream, EXCEL_MEDIA_TYPE, "reporte_inventario.xlsx")


# ===================== PDF =====================

PDF_HEADERS = ["SKU", "Producto", "Categoría", "Stock", "Mínimo", "P. Costo", "P. Venta", "Estado"]
PDF_WIDTHS = [2.6 * cm, 6.5 * cm, 3.8 * cm, 2 * cm, 2 * cm, 3.2 * cm, 3.2 * cm, 2.4 * cm]


def pdf_product_row(product: dict) -> list:
    return [
        product.get("sku", ""),
        product.get("name", ""),
        product.get("category", ""),
        str(product.get("currentStock", 0)),
        str(product.get("minStock", 0)),
        money(float(product.get("costPrice", 0))),
        money(float(product.get("salePrice", 0))),
        "CRÍTICO" if is_critical(product) else "OK",
    ]


def products_table(products: list, header_color: str) -> Table:
    table = Table([PDF_HEADERS] + [pdf_product_row(p) for p in products], colWidths=PDF_WIDTHS, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(f"#{header_color}")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("ALIGN", (3, 0), (-1, -1), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor(f"#{GRAY_LIGHT}")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]
    for index, product in enumerate(products, start=1):
        if is_critical(product):
            style.append(("TEXTCOLOR", (7, index), (7, index), colors.HexColor(f"#{RED}")))
            style.append(("FONTNAME", (7, index), (7, index), "Helvetica-Bold"))
    table.setStyle(TableStyle(style))
    return table


def summary_table(metrics: dict, critical_count: int) -> Table:
    labels = ["Productos", "Unidades", "En stock crítico", "Valorización a costo", "Valorización a venta"]
    values = [
        str(metrics["total_items"]),
        str(metrics["total_units"]),
        str(critical_count),
        money(metrics["cost_value"]),
        money(metrics["sale_value"]),
    ]
    table = Table([labels, values], colWidths=[5.1 * cm] * 5)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(f"#{GRAY_LIGHT}")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#6B7280")),
        ("FONTSIZE", (0, 0), (-1, 0), 8),
        ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 1), (-1, 1), 13),
        ("TEXTCOLOR", (2, 1), (2, 1), colors.HexColor(f"#{RED}")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
        ("TOPPADDING", (0, 1), (-1, 1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 8),
    ]))
    return table


def draw_page_header(canvas, doc) -> None:
    width, height = doc.pagesize
    canvas.saveState()
    canvas.setFillColor(colors.HexColor(f"#{DARK}"))
    canvas.rect(0, height - 2 * cm, width, 2 * cm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor(f"#{GREEN}"))
    canvas.setFont("Helvetica-Bold", 16)
    canvas.drawString(1.5 * cm, height - 1.25 * cm, "AutoStock")
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica", 11)
    canvas.drawString(4.6 * cm, height - 1.25 * cm, "Reporte de Inventario")
    canvas.drawRightString(width - 1.5 * cm, height - 1.25 * cm, datetime.now().strftime("%d/%m/%Y %H:%M"))
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(width - 1.5 * cm, 1 * cm, f"Página {doc.page}")
    canvas.restoreState()


def section_title(text: str, color: str) -> Paragraph:
    style = getSampleStyleSheet()["Heading3"]
    style.textColor = colors.HexColor(f"#{color}")
    return Paragraph(text, style)


def build_pdf_story(products: list) -> list:
    critical = [p for p in products if is_critical(p)]
    story = [summary_table(inventory_metrics(products), len(critical)), Spacer(1, 0.6 * cm)]
    story.append(section_title(f"Reposición urgente ({len(critical)})", RED))
    story.append(products_table(critical, RED) if critical else Paragraph("Sin productos en stock crítico.", getSampleStyleSheet()["Normal"]))
    story += [Spacer(1, 0.6 * cm), section_title(f"Detalle de productos ({len(products)})", GREEN)]
    story.append(products_table(products, GREEN) if products else Paragraph("Sin productos cargados.", getSampleStyleSheet()["Normal"]))
    return story


@router.get("/pdf")
async def get_pdf_report():
    products = await load_products()

    stream = io.BytesIO()
    doc = SimpleDocTemplate(
        stream, pagesize=landscape(A4),
        topMargin=2.6 * cm, bottomMargin=1.6 * cm, leftMargin=1.5 * cm, rightMargin=1.5 * cm,
    )
    doc.build(build_pdf_story(products), onFirstPage=draw_page_header, onLaterPages=draw_page_header)

    return file_response(stream, "application/pdf", "reporte_inventario.pdf")