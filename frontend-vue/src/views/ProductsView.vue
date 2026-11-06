<template>
  <div style="padding: 2rem; font-family: sans-serif; max-width: 1200px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
      <h1 style="color: #333; margin: 0;">Catálogo de Productos</h1>
      <div style="display: flex; gap: 0.5rem;">
        <button @click="exportToExcel" style="background-color: #198754; color: white; border: none; padding: 0.5rem 0.9rem; border-radius: 6px; font-weight: bold; cursor: pointer;">📊 Exportar a Excel</button>
        <button @click="exportToPDF" style="background-color: #0d6efd; color: white; border: none; padding: 0.5rem 0.9rem; border-radius: 6px; font-weight: bold; cursor: pointer;">📄 Exportar a PDF</button>
        <button @click="goCriticalStock" style="padding: 0.5rem 1rem; background-color: #dc3545; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; display: flex; align-items: center; gap: 0.3rem;">
          ⚠️ Stock Crítico
        </button>
        <button @click="openCreateModal" style="padding: 0.5rem 1rem; background-color: #198754; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
          + Nuevo Producto
        </button>
        <button @click="handleLogout" style="padding: 0.5rem 1rem; background-color: #6c757d; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
          Cerrar Sesión
        </button>
      </div>
    </div>

    <!-- Filtros de Búsqueda -->
    <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem; background: #fff; padding: 1rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
      <div style="flex: 2;">
        <label style="display: block; margin-bottom: 0.4rem; font-size: 0.9rem; font-weight: bold;">Buscar (SKU / Nombre)</label>
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Ej: ART-001 o Aceite..."
          style="width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ced4da; border-radius: 4px;"
        />
      </div>

      <div style="flex: 1;">
        <label style="display: block; margin-bottom: 0.4rem; font-size: 0.9rem; font-weight: bold;">Categoría</label>
        <select
          v-model="selectedCategory"
          style="width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ced4da; border-radius: 4px; background: white;"
        >
          <option value="">Todas las categorías</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
    </div>

    <!-- Indicador de Carga -->
    <div v-if="loading" style="text-align: center; padding: 2rem; color: #007bff; font-weight: bold;">
      Cargando catálogo...
    </div>

    <!-- Componente Tabla -->
    <ProductTable v-else :products="filteredProducts" @edit="openEditModal" @adjust-stock="openStockModal" />

    <!-- Modal Formulario de Producto -->
    <ProductFormModal
      :isOpen="isModalOpen"
      :productToEdit="editingProduct"
      @close="isModalOpen = false"
      @saved="handleProductSaved"
    />

    <!-- Modal Ajuste de Stock -->
    <StockAdjustmentModal
      :isOpen="isStockModalOpen"
      :product="stockProduct"
      @close="isStockModalOpen = false"
      @adjusted="handleStockAdjusted"
    />
  </div>
</template>

<script setup>
import * as XLSX from 'xlsx';
import jsPDF from 'jspdf';
import autoTable from 'jspdf-autotable';

import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axiosClient from '../api/axiosClient';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import { getLocalProducts, saveLocalProducts } from '../services/storage';

const router = useRouter();
const products = ref([]);
const searchQuery = ref('');
const selectedCategory = ref('');
const loading = ref(true);

const isModalOpen = ref(false);
const editingProduct = ref(null);

const isStockModalOpen = ref(false);
const stockProduct = ref(null);

const fetchProducts = async () => {
  loading.value = true;
  try {
    const response = await axiosClient.get('/products');
    const data = Array.isArray(response.data) ? response.data : (response.data.products || []);
    if (data.length > 0) {
      products.value = data;
      saveLocalProducts(data);
    } else {
      products.value = getLocalProducts();
    }
  } catch (err) {
    products.value = getLocalProducts();
  } finally {
    loading.value = false;
  }
};

const categories = computed(() => {
  const cats = products.value.map(p => p.category || p.categoria).filter(Boolean);
  return [...new Set(cats)];
});

const filteredProducts = computed(() => {
  return products.value.filter(product => {
    const name = (product.name || product.nombre || '').toLowerCase();
    const sku = (product.sku || '').toLowerCase();
    const query = searchQuery.value.toLowerCase();

    const matchesSearch = name.includes(query) || sku.includes(query);
    const matchesCategory = !selectedCategory.value || (product.category || product.categoria) === selectedCategory.value;

    return matchesSearch && matchesCategory;
  });
});

const goCriticalStock = () => {
  router.push('/critical-stock');
};

const openCreateModal = () => {
  editingProduct.value = null;
  isModalOpen.value = true;
};

const openEditModal = (product) => {
  editingProduct.value = product;
  isModalOpen.value = true;
};

const openStockModal = (product) => {
  stockProduct.value = product;
  isStockModalOpen.value = true;
};

const handleProductSaved = (savedProduct) => {
  const targetId = savedProduct._id || savedProduct.id;
  const index = products.value.findIndex(p => (p._id || p.id) === targetId);

  if (index !== -1) {
    products.value[index] = { ...savedProduct };
    products.value = [...products.value];
  } else {
    products.value = [savedProduct, ...products.value];
  }
  saveLocalProducts(products.value);
};

const handleStockAdjusted = (updatedProduct) => {
  const targetId = updatedProduct._id || updatedProduct.id;
  const index = products.value.findIndex(p => (p._id || p.id) === targetId);

  if (index !== -1) {
    products.value[index] = { ...products.value[index], stock: updatedProduct.stock };
    products.value = [...products.value];
    saveLocalProducts(products.value);
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchProducts();
});

const exportToExcel = () => {
  const allProducts = typeof products !== 'undefined' ? products.value : [];
  if (!allProducts || allProducts.length === 0) return alert('No hay productos en el inventario para exportar');
  
  const data = allProducts.map(p => ({
    SKU: String(p.sku || 'N/A'),
    Producto: String(p.name || p.nombre || 'Sin nombre'),
    Categoría: String(p.category || p.categoria || 'General'),
    Precio: Number(p.price || p.precio || 0),
    Stock: Number(p.stock || 0)
  }));

  const worksheet = XLSX.utils.json_to_sheet(data);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Inventario');
  XLSX.writeFile(workbook, 'Reporte_Inventario_General.xlsx');
};

const exportToPDF = () => {
  const allProducts = typeof products !== 'undefined' ? products.value : [];
  if (!allProducts || allProducts.length === 0) return alert('No hay productos en el inventario para exportar');

  try {
    const doc = new jsPDF();
    const today = new Date().toLocaleDateString('es-AR', { year: 'numeric', month: 'long', day: 'numeric' });

    doc.setFillColor(15, 23, 42);
    doc.rect(0, 0, 210, 28, 'F');
    
    doc.setTextColor(255, 255, 255);
    doc.setFontSize(16);
    doc.setFont('helvetica', 'bold');
    doc.text('AUTOSTOCK', 14, 18);
    
    doc.setFontSize(10);
    doc.setFont('helvetica', 'normal');
    doc.text('REPORTE GENERAL DE INVENTARIO', 196, 18, { align: 'right' });

    doc.setTextColor(100, 116, 139);
    doc.setFontSize(9);
    doc.text(`Fecha de emisión: ${today}`, 14, 35);
    doc.text(`Total de items: ${allProducts.length}`, 196, 35, { align: 'right' });

    const tableData = allProducts.map(p => [
      String(p.sku || 'N/A'),
      String(p.name || p.nombre || 'Sin nombre'),
      String(p.category || p.categoria || 'General'),
      '$ ' + Number(p.price || p.precio || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }),
      String(p.stock || 0) + ' u.'
    ]);

    autoTable(doc, {
      startY: 40,
      head: [['SKU', 'Producto', 'Categoría', 'Precio', 'Stock']],
      body: tableData,
      theme: 'grid',
      headStyles: { fillColor: [30, 41, 59], textColor: [255, 255, 255], fontStyle: 'bold', fontSize: 10 },
      bodyStyles: { textColor: [51, 65, 85], fontSize: 9 },
      alternateRowStyles: { fillColor: [248, 250, 252] },
      columnStyles: { 3: { halign: 'right' }, 4: { halign: 'center' } }
    });

    doc.save('Reporte_Inventario_General.pdf');
  } catch (error) {
    console.error('Error al generar PDF:', error);
    alert('Error al generar PDF: ' + error.message);
  }
};

</script>
