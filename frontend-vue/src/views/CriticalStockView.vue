<template>
  <div style="padding: 2rem; font-family: sans-serif; max-width: 1200px; margin: 0 auto;">
    <!-- Header -->
    <div style="margin-bottom: 1.5rem;">
      <h1 style="color: #dc3545; margin: 0;">Productos en Stock Critico</h1>
      <p style="color: #6c757d; margin: 0.3rem 0 0 0;">Articulos con existencias menores o iguales a 5 unidades.</p>
    </div>

    <!-- Botones de Exportacion -->
    <div style="display: flex; gap: 0.75rem; margin-bottom: 1.5rem;">
      <button 
        @click="exportToExcel" 
        style="background-color: #198754; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem;"
      >
        📊 Exportar Excel (General)
      </button>
      <button 
        @click="exportToPDF" 
        style="background-color: #0d6efd; color: white; border: none; padding: 0.6rem 1.2rem; border-radius: 6px; font-weight: bold; cursor: pointer; display: inline-flex; align-items: center; gap: 0.5rem;"
      >
        📄 Exportar PDF (General)
      </button>
    </div>

    <!-- Alerta vacia -->
    <div v-if="criticalProducts.length === 0" style="padding: 1.5rem; background: #e8f5e9; color: #2e7d32; border-radius: 6px; font-weight: bold; text-align: center;">
      Todos los productos cuentan con niveles de stock adecuados.
    </div>

    <!-- Tabla -->
    <div v-else style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; background: white;">
      <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <thead>
          <tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">
            <th style="padding: 0.75rem 1rem;">SKU</th>
            <th style="padding: 0.75rem 1rem;">Producto</th>
            <th style="padding: 0.75rem 1rem;">Categoria</th>
            <th style="padding: 0.75rem 1rem; text-align: right;">Precio</th>
            <th style="padding: 0.75rem 1rem; text-align: center;">Stock</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in criticalProducts" :key="p.sku || p.id" style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 0.75rem 1rem; font-weight: bold;">{{ p.sku || 'N/A' }}</td>
            <td style="padding: 0.75rem 1rem;">{{ p.name || p.nombre || 'Sin nombre' }}</td>
            <td style="padding: 0.75rem 1rem;">{{ p.category || p.categoria || 'General' }}</td>
            <td style="padding: 0.75rem 1rem; text-align: right;">$ {{ Number(p.price || p.precio || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }) }}</td>
            <td style="padding: 0.75rem 1rem; text-align: center;">
              <span style="background-color: #dc3545; color: white; padding: 0.25rem 0.6rem; border-radius: 12px; font-weight: bold; font-size: 0.85rem;">
                {{ p.stock }} u.
              </span>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getLocalProducts } from '../services/storage';
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

const products = ref([]);

onMounted(() => {
  const data = getLocalProducts();
  products.value = Array.isArray(data) ? data : [];
});

const criticalProducts = computed(() => {
  return products.value.filter(p => Number(p.stock) <= 5);
});

const exportToExcel = () => {
  if (products.value.length === 0) return alert('No hay productos en el inventario para exportar');
  
  const data = products.value.map(p => ({
    SKU: String(p.sku || 'N/A'),
    Producto: String(p.name || p.nombre || 'Sin nombre'),
    Categoria: String(p.category || p.categoria || 'General'),
    Precio: Number(p.price || p.precio || 0),
    Stock: Number(p.stock || 0)
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Inventario');
  XLSX.writeFile(workbook, 'Reporte_Inventario_General.xlsx');
};

const exportToPDF = () => {
  if (products.value.length === 0) return alert('No hay productos en el inventario para exportar');

  try {
    const doc = new jsPDF();
    const today = new Date().toLocaleDateString('es-AR', { year: 'numeric', month: 'long', day: 'numeric' });

    // Header superior
    doc.setFillColor(15, 23, 42); // Azul noche elegante #0f172a
    doc.rect(0, 0, 210, 28, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('AUTOSTOCK', 14, 18);
    
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text('REPORTE GENERAL DE INVENTARIO', 196, 18, { align: 'right' });

    // Meta datos del reporte
    doc.setTextColor(100, 116, 139);
    doc.setFontSize(9);
    doc.text(`Fecha de emision: ${today}`, 14, 35);
    doc.text(`Total de items: ${products.value.length}`, 196, 35, { align: 'right' });

    // Preparar filas de la tabla
    const tableData = products.value.map(p => [
      String(p.sku || 'N/A'),
      String(p.name || p.nombre || 'Sin nombre'),
      String(p.category || p.categoria || 'General'),
      '$ ' + Number(p.price || p.precio || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }),
      String(p.stock || 0) + ' u.'
    ]);

    // Tabla estilizada
    autoTable(doc, {
      startY: 40,
      head: [['SKU', 'Producto', 'Categoria', 'Precio', 'Stock']],
      body: tableData,
      theme: 'grid',
      headStyles: { 
        fillColor: [30, 41, 59], 
        textColor: [255, 255, 255], 
        fontStyle: 'bold',
        fontSize: 10,
        cellPadding: 4
      },
      bodyStyles: { 
        textColor: [51, 65, 85], 
        fontSize: 9,
        cellPadding: 3.5
      },
      alternateRowStyles: { 
        fillColor: [248, 250, 252] 
      },
      columnStyles: {
        3: { halign: 'right' },
        4: { halign: 'center' }
      },
      didDrawPage: function (data) {
        // Pie de pagina
        const pageCount = doc.internal.getNumberOfPages();
        doc.setFontSize(8);
        doc.setTextColor(148, 163, 184);
        doc.text(`Pagina ${data.pageNumber} de ${pageCount}`, 196, 287, { align: 'right' });
        doc.text('AutoStock System — Documento de uso interno', 14, 287);
      }
    });

    doc.save('Reporte_Inventario_General.pdf');
  } catch (error) {
    console.error('Error al generar PDF:', error);
    alert('Error al generar PDF: ' + error.message);
  }
};
</script>