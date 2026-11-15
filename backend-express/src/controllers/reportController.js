const ExcelJS = require('exceljs');
const PDFDocument = require('pdfkit');
const Product = require('../models/Product');

const EXCEL_MEDIA_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet';
const MONEY_FORMAT = '"$" #,##0.00';

// Colores compartidos (mismos que el frontend y FastAPI)
const GREEN = '16A34A';
const RED = 'DC2626';
const RED_LIGHT = 'FDE2E2';
const GRAY_LIGHT = 'F3F4F6';
const DARK = '1E222B';

const EXCEL_COLUMNS = [
  { header: 'SKU', key: 'sku', width: 14 },
  { header: 'Nombre', key: 'name', width: 32 },
  { header: 'Categoría', key: 'category', width: 18 },
  { header: 'Precio Costo', key: 'costPrice', width: 16, style: { numFmt: MONEY_FORMAT } },
  { header: 'Precio Venta', key: 'salePrice', width: 16, style: { numFmt: MONEY_FORMAT } },
  { header: 'Stock Actual', key: 'currentStock', width: 14 },
  { header: 'Stock Mínimo', key: 'minStock', width: 14 },
  { header: 'Estado', key: 'status', width: 12 },
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
  criticalCount: products.filter(isCritical).length,
  costValue: products.reduce((acc, p) => acc + (p.costPrice || 0) * (p.currentStock || 0), 0),
  saleValue: products.reduce((acc, p) => acc + (p.salePrice || 0) * (p.currentStock || 0), 0),
});

// Formato argentino: $ 1.234,56
const money = (value) =>
  `$ ${Number(value || 0).toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}`;

const formatDate = () => {
  const d = new Date();
  const pad = (n) => String(n).padStart(2, '0');
  return `${pad(d.getDate())}/${pad(d.getMonth() + 1)}/${d.getFullYear()} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
};

const setDownloadHeaders = (res, mediaType, filename) => {
  res.setHeader('Content-Type', mediaType);
  res.setHeader('Content-Disposition', `attachment; filename="${filename}"`);
};

// ===================== EXCEL =====================

const fill = (color) => ({ type: 'pattern', pattern: 'solid', fgColor: { argb: `FF${color}` } });

const styleHeader = (worksheet) => {
  const header = worksheet.getRow(1);
  header.height = 22;
  header.eachCell((cell) => {
    cell.font = { bold: true, color: { argb: 'FFFFFFFF' } };
    cell.fill = fill(GREEN);
    cell.alignment = { horizontal: 'center', vertical: 'middle' };
  });
  worksheet.views = [{ state: 'frozen', ySplit: 1 }];
};

const styleProductRow = (row, critical) => {
  row.eachCell((cell) => {
    cell.border = { bottom: { style: 'thin', color: { argb: 'FFE5E7EB' } } };
    if (critical) cell.fill = fill(RED_LIGHT);
  });
  const status = row.getCell('status');
  status.font = { bold: true, color: { argb: `FF${critical ? RED : GREEN}` } };
  status.alignment = { horizontal: 'center' };
};

const writeInventorySheet = (workbook, products) => {
  const worksheet = workbook.addWorksheet('Inventario');
  worksheet.columns = EXCEL_COLUMNS;
  styleHeader(worksheet);
  products.forEach((p) => styleProductRow(worksheet.addRow(productRow(p)), isCritical(p)));
  worksheet.autoFilter = { from: 'A1', to: { row: 1, column: EXCEL_COLUMNS.length } };
};

const writeSummarySheet = (workbook, products) => {
  const metrics = inventoryMetrics(products);
  const worksheet = workbook.addWorksheet('Resumen');
  worksheet.columns = [{ width: 30 }, { width: 22 }];
  worksheet.addRows([
    ['Reporte de Inventario - AutoStock'],
    ['Generado', formatDate()],
    ['Total de productos', metrics.totalItems],
    ['Unidades en stock', metrics.totalUnits],
    ['Productos en stock crítico', metrics.criticalCount],
    ['Valorización a costo', metrics.costValue],
    ['Valorización a venta', metrics.saleValue],
  ]);
  worksheet.getCell('A1').font = { bold: true, size: 14, color: { argb: `FF${GREEN}` } };
  ['B6', 'B7'].forEach((ref) => { worksheet.getCell(ref).numFmt = MONEY_FORMAT; });
  for (let i = 2; i <= 7; i += 1) worksheet.getCell(`A${i}`).font = { bold: true };
};

const getExcelReport = async (req, res) => {
  try {
    const products = await loadProducts();
    const workbook = new ExcelJS.Workbook();
    writeInventorySheet(workbook, products);
    writeSummarySheet(workbook, products);

    setDownloadHeaders(res, EXCEL_MEDIA_TYPE, 'reporte_inventario.xlsx');
    await workbook.xlsx.write(res);
    return res.end();
  } catch (error) {
    return res.status(500).json({ detail: 'Error al generar el reporte Excel' });
  }
};

// ===================== PDF =====================

const PAGE_MARGIN = 42;
const ROW_HEIGHT = 20;
const PDF_COLUMNS = [
  { header: 'SKU', width: 74, value: (p) => p.sku || '' },
  { header: 'Producto', width: 184, value: (p) => p.name || '' },
  { header: 'Categoría', width: 108, value: (p) => p.category || '' },
  { header: 'Stock', width: 57, value: (p) => String(p.currentStock || 0), align: 'center' },
  { header: 'Mínimo', width: 57, value: (p) => String(p.minStock || 0), align: 'center' },
  { header: 'P. Costo', width: 91, value: (p) => money(p.costPrice), align: 'center' },
  { header: 'P. Venta', width: 91, value: (p) => money(p.salePrice), align: 'center' },
  { header: 'Estado', width: 68, value: (p) => (isCritical(p) ? 'CRÍTICO' : 'OK'), align: 'center' },
];
const TABLE_WIDTH = PDF_COLUMNS.reduce((acc, c) => acc + c.width, 0);

const drawPageHeader = (doc, pageNumber) => {
  const { width } = doc.page;
  doc.save();
  doc.rect(0, 0, width, 56).fill(`#${DARK}`);
  doc.fillColor(`#${GREEN}`).font('Helvetica-Bold').fontSize(16).text('AutoStock', PAGE_MARGIN, 20, { lineBreak: false });
  doc.fillColor('white').font('Helvetica').fontSize(11).text('Reporte de Inventario', 130, 23, { lineBreak: false });
  doc.text(`${formatDate()}  ·  Página ${pageNumber}`, width - PAGE_MARGIN - 220, 23, { width: 220, align: 'right', lineBreak: false });
  doc.restore();
  doc.y = 76;
};

const drawRow = (doc, cells, { background, color = '#111827', bold = false, statusColor }) => {
  const y = doc.y;
  doc.rect(PAGE_MARGIN, y, TABLE_WIDTH, ROW_HEIGHT).fillAndStroke(background, '#D1D5DB');
  let x = PAGE_MARGIN;
  PDF_COLUMNS.forEach((column, index) => {
    const isStatus = index === PDF_COLUMNS.length - 1;
    doc.fillColor(isStatus && statusColor ? statusColor : color)
      .font(bold || (isStatus && statusColor) ? 'Helvetica-Bold' : 'Helvetica').fontSize(9)
      .text(cells[index], x + 5, y + 6, { width: column.width - 10, align: column.align || 'left', lineBreak: false });
    x += column.width;
  });
  doc.y = y + ROW_HEIGHT;
};

const ensureSpace = (doc, headerColor) => {
  if (doc.y + ROW_HEIGHT <= doc.page.height - PAGE_MARGIN) return;
  doc.addPage();
  drawRow(doc, PDF_COLUMNS.map((c) => c.header), { background: `#${headerColor}`, color: 'white', bold: true });
};

const drawProductsTable = (doc, products, headerColor) => {
  drawRow(doc, PDF_COLUMNS.map((c) => c.header), { background: `#${headerColor}`, color: 'white', bold: true });
  products.forEach((p, index) => {
    ensureSpace(doc, headerColor);
    drawRow(doc, PDF_COLUMNS.map((c) => c.value(p)), {
      background: index % 2 === 0 ? 'white' : `#${GRAY_LIGHT}`,
      statusColor: isCritical(p) ? `#${RED}` : null,
    });
  });
};

const drawSummary = (doc, metrics) => {
  const items = [
    ['Productos', String(metrics.totalItems)],
    ['Unidades', String(metrics.totalUnits)],
    ['En stock crítico', String(metrics.criticalCount)],
    ['Valorización a costo', money(metrics.costValue)],
    ['Valorización a venta', money(metrics.saleValue)],
  ];
  const boxWidth = TABLE_WIDTH / items.length;
  const y = doc.y;
  doc.rect(PAGE_MARGIN, y, TABLE_WIDTH, 50).fillAndStroke(`#${GRAY_LIGHT}`, '#D1D5DB');
  items.forEach(([label, value], index) => {
    const x = PAGE_MARGIN + index * boxWidth;
    doc.fillColor('#6B7280').font('Helvetica').fontSize(8).text(label, x, y + 9, { width: boxWidth, align: 'center' });
    doc.fillColor(index === 2 ? `#${RED}` : '#111827').font('Helvetica-Bold').fontSize(13)
      .text(value, x, y + 24, { width: boxWidth, align: 'center' });
  });
  doc.y = y + 70;
};

const drawSection = (doc, title, products, color, emptyText) => {
  doc.fillColor(`#${color}`).font('Helvetica-Bold').fontSize(12).text(title, PAGE_MARGIN, doc.y);
  doc.moveDown(0.4);
  if (products.length === 0) {
    doc.fillColor('#111827').font('Helvetica').fontSize(10).text(emptyText, PAGE_MARGIN, doc.y);
  } else {
    drawProductsTable(doc, products, color);
  }
  doc.y += 20;
};

const getPDFReport = async (req, res) => {
  try {
    const products = await loadProducts();
    const critical = products.filter(isCritical);
    const doc = new PDFDocument({ size: 'A4', layout: 'landscape', margin: PAGE_MARGIN });

    setDownloadHeaders(res, 'application/pdf', 'reporte_inventario.pdf');
    doc.pipe(res);
    let pageNumber = 1;
    doc.on('pageAdded', () => { pageNumber += 1; drawPageHeader(doc, pageNumber); });
    drawPageHeader(doc, pageNumber);
    drawSummary(doc, inventoryMetrics(products));
    drawSection(doc, `Reposición urgente (${critical.length})`, critical, RED, 'Sin productos en stock crítico.');
    drawSection(doc, `Detalle de productos (${products.length})`, products, GREEN, 'Sin productos cargados.');
    doc.end();
    return undefined;
  } catch (error) {
    return res.status(500).json({ detail: 'Error al generar el reporte PDF' });
  }
};

module.exports = { getExcelReport, getPDFReport };