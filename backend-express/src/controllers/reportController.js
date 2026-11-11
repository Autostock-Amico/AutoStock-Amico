const ExcelJS = require('exceljs');
const PDFDocument = require('pdfkit');
const Product = require('../models/Product');

const EXCEL_MEDIA_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';

const EXCEL_COLUMNS = [
  { header: 'SKU', key: 'sku', width: 12 },
  { header: 'Nombre', key: 'name', width: 30 },
  { header: 'Categoría', key: 'category', width: 18 },
  { header: 'Precio Costo', key: 'costPrice', width: 14 },
  { header: 'Precio Venta', key: 'salePrice', width: 14 },
  { header: 'Stock Actual', key: 'currentStock', width: 14 },
  { header: 'Stock Mínimo', key: 'minStock', width: 14 },
  { header: 'Estado', key: 'status', width: 10 },
];

const isCritical = (p) => (p.currentStock || 0) <= (p.minStock || 0);

const loadProducts = () => Product.find().sort({ name: 1 }).lean();

const productRow = (p) => ({
  sku: p.sku || '',
  name: p.name || '',
  category: p.category || '',
  costPrice: Number(p.costPrice || 0),
  salePrice: Number(p.salePrice || 0),
  currentStock: Number(p.currentStock || 0),
  minStock: Number(p.minStock || 0),
  status: isCritical(p) ? 'CRÍTICO' : 'OK',
});

const inventoryMetrics = (products) => ({
  totalItems: products.length,
  totalUnits: products.reduce((acc, p) => acc + (p.currentStock || 0), 0),
  costValue: products.reduce((acc, p) => acc + (p.costPrice || 0) * (p.currentStock || 0), 0),
  saleValue: products.reduce((acc, p) => acc + (p.salePrice || 0) * (p.currentStock || 0), 0),
});

const money = (value) => value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

const setDownloadHeaders = (res, mediaType, filename) => {
  res.setHeader('Content-Type', mediaType);
  res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
};

const getExcelReport = async (req, res) => {
  try {
    const products = await loadProducts();
    const workbook = new ExcelJS.Workbook();
    const worksheet = workbook.addWorksheet('Inventario');
    worksheet.columns = EXCEL_COLUMNS;
    products.forEach((p) => worksheet.addRow(productRow(p)));

    setDownloadHeaders(res, EXCEL_MEDIA_TYPE, 'reporte_inventario.xlsx');
    await workbook.xlsx.write(res);
    return res.end();
  } catch (error) {
    return res.status(500).json({ detail: 'Error al generar el reporte Excel' });
  }
};

const writeSummary = (doc, metrics) => {
  doc.fontSize(16).text('Reporte de Inventario - AutoStock');
  doc.moveDown();
  doc.fontSize(12);
  doc.text(`Total de productos: ${metrics.totalItems}`);
  doc.text(`Unidades en stock: ${metrics.totalUnits}`);
  doc.text(`Valorización a costo: $${money(metrics.costValue)}`);
  doc.text(`Valorización a venta: $${money(metrics.saleValue)}`);
  doc.moveDown();
};

const writeProductList = (doc, title, products) => {
  doc.fontSize(12).text(title);
  doc.moveDown(0.5);
  doc.fontSize(10);
  if (products.length === 0) doc.text('Sin productos.');
  products.forEach((p) => {
    doc.text(
      `${p.sku || ''} | ${p.name || ''} | Cat: ${p.category || ''} | ` +
      `Stock: ${p.currentStock || 0} (mín. ${p.minStock || 0}) | Venta: $${p.salePrice || 0}`
    );
  });
  doc.moveDown();
};

const getPDFReport = async (req, res) => {
  try {
    const products = await loadProducts();
    const doc = new PDFDocument({ margin: 50 });

    setDownloadHeaders(res, 'application/pdf', 'reporte_inventario.pdf');
    doc.pipe(res);
    writeSummary(doc, inventoryMetrics(products));
    writeProductList(doc, 'Reposición urgente (stock crítico):', products.filter(isCritical));
    writeProductList(doc, 'Detalle de productos:', products);
    doc.end();
    return undefined;
  } catch (error) {
    return res.status(500).json({ detail: 'Error al generar el reporte PDF' });
  }
};

module.exports = { getExcelReport, getPDFReport };
