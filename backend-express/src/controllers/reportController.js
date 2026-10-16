const ExcelJS = require('exceljs');
const PDFDocument = require('pdfkit');
const Product = require('../models/Product');

// GET /api/reports/excel
exports.getExcelReport = async (req, res) => {
  try {
    const products = await Product.find().lean();

    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Inventario');

    worksheet.columns = [
      { header: 'Nombre', key: 'name', width: 25 },
      { header: 'Categoría', key: 'category', width: 15 },
      { header: 'Precio', key: 'price', width: 12 },
      { header: 'Stock Actual', key: 'stock', width: 15 },
      { header: 'Stock Mínimo', key: 'minStock', width: 15 },
    ];

    products.forEach((prod) => {
      worksheet.addRow({
        name: prod.name || 'N/A',
        category: prod.category || 'N/A',
        price: prod.price || 0,
        stock: prod.stock || 0,
        minStock: prod.minStock || 0,
      });
    });

    res.setHeader(
      'Content-Type',
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    );
    res.setHeader(
      'Content-Disposition',
      'attachment; filename="reporte_inventario.xlsx"'
    );

    await workbook.xlsx.write(res);
    res.end();
  } catch (error) {
    res.status(500).json({ message: 'Error al generar reporte Excel', error: error.message });
  }
};

// GET /api/reports/pdf
exports.getPDFReport = async (req, res) => {
  try {
    const products = await Product.find().lean();

    const doc = new PDFDocument({ margin: 30 });

    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader(
      'Content-Disposition',
      'attachment; filename="reporte_inventario.pdf"'
    );

    doc.pipe(res);

    doc.fontSize(18).text('Reporte de Resumen de Inventario', { align: 'center' });
    doc.moveDown();

    const totalProductos = products.length;
    const totalStock = products.reduce((acc, p) => acc + (p.stock || 0), 0);
    const valorTotal = products.reduce((acc, p) => acc + ((p.price || 0) * (p.stock || 0)), 0);

    doc.fontSize(12).text(`Total de ítems registrados: ${totalProductos}`);
    doc.text(`Unidades en stock total: ${totalStock}`);
    doc.text(`Valoración estimativa del inventario: $${valorTotal.toFixed(2)}`);
    doc.moveDown();

    doc.fontSize(14).text('Detalle de Productos:', { underline: true });
    doc.moveDown(0.5);

    products.forEach((prod, index) => {
      doc.fontSize(10).text(
        `${index + 1}. ${prod.name || 'Sin nombre'} | Cat: ${prod.category || 'N/A'} | Stock: ${prod.stock || 0} | Precio: $${prod.price || 0}`
      );
    });

    doc.end();
  } catch (error) {
    res.status(500).json({ message: 'Error al generar reporte PDF', error: error.message });
  }
};
