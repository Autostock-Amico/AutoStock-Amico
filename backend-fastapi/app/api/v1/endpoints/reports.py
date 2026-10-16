import io
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from openpyxl import Workbook
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from app.core.database import db

router = APIRouter()

@router.get("/excel")
async def get_excel_report():
    try:
        products = await db["products"].find().to_list(1000)

        wb = Workbook()
        ws = wb.active
        ws.title = "Inventario"

        ws.append(["Nombre", "Categoría", "Precio", "Stock Actual", "Stock Mínimo"])

        for prod in products:
            ws.append([
                str(prod.get("name", "N/A")),
                str(prod.get("category", "N/A")),
                float(prod.get("price", 0)),
                int(prod.get("stock", 0)),
                int(prod.get("minStock", 0))
            ])

        stream = io.BytesIO()
        wb.save(stream)
        stream.seek(0)

        headers = {
            'Content-Disposition': 'attachment; filename="reporte_inventario.xlsx"'
        }

        return StreamingResponse(
            stream,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/pdf")
async def get_pdf_report():
    try:
        products = await db["products"].find().to_list(1000)

        stream = io.BytesIO()
        p = canvas.Canvas(stream, pagesize=letter)
        
        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, 750, "Reporte de Resumen de Inventario (FastAPI)")

        total_productos = len(products)
        total_stock = sum(int(p_item.get("stock", 0)) for p_item in products)
        valor_total = sum(float(p_item.get("price", 0)) * int(p_item.get("stock", 0)) for p_item in products)

        p.setFont("Helvetica", 12)
        p.drawString(100, 720, f"Total de ítems registrados: {total_productos}")
        p.drawString(100, 705, f"Unidades en stock total: {total_stock}")
        p.drawString(100, 690, f"Valoración estimativa del inventario: ${valor_total:.2f}")

        y = 650
        p.setFont("Helvetica-Bold", 12)
        p.drawString(100, y, "Detalle de Productos:")
        y -= 20

        p.setFont("Helvetica", 10)
        for idx, prod in enumerate(products, 1):
            linea = f"{idx}. {prod.get('name', 'N/A')} | Cat: {prod.get('category', 'N/A')} | Stock: {prod.get('stock', 0)} | Precio: ${prod.get('price', 0)}"
            p.drawString(100, y, linea)
            y -= 15
            if y < 50:
                p.showPage()
                y = 750

        p.save()
        stream.seek(0)

        headers = {
            'Content-Disposition': 'attachment; filename="reporte_inventario.pdf"'
        }

        return StreamingResponse(
            stream,
            media_type="application/pdf",
            headers=headers
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
