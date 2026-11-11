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
    <div v-else-if="errorMessage" style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 4px; margin-bottom: 1rem;">
      {{ errorMessage }}
    </div>

    <ProductTable
      v-if="!loading"
      :products="filteredProducts"
      @edit="openEditModal"
      @adjust-stock="openStockModal"
      @delete="handleDelete"
    />

    <!-- Modal Formulario de Producto -->
    <ProductFormModal
      :isOpen="isModalOpen"
      :productToEdit="editingProduct"
      :categories="categories"
      @close="isModalOpen = false"
      @saved="handleProductSaved"
    />

    <!-- Modal Ajuste de Stock -->
    <StockAdjustmentModal
      :isOpen="isStockModalOpen"
      :product="stockProduct"
      @close="isStockModalOpen = false"
      @adjusted="handleProductSaved"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import {
  getProducts,
  deleteProduct,
  downloadExcelReport,
  downloadPdfReport,
  getApiErrorMessage
} from '../services/productService';

const router = useRouter();
const products = ref([]);
const searchQuery = ref('');
const selectedCategory = ref('');
const loading = ref(true);
const errorMessage = ref('');

const isModalOpen = ref(false);
const editingProduct = ref(null);

const isStockModalOpen = ref(false);
const stockProduct = ref(null);

const fetchProducts = async () => {
  loading.value = true;
  errorMessage.value = '';
  try {
    products.value = await getProducts();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudieron cargar los productos.');
  } finally {
    loading.value = false;
  }
};

const categories = computed(() => [...new Set(products.value.map(p => p.category).filter(Boolean))]);

const filteredProducts = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return products.value.filter(p => {
    const matchesSearch = p.name.toLowerCase().includes(query) || p.sku.toLowerCase().includes(query);
    const matchesCategory = !selectedCategory.value || p.category === selectedCategory.value;
    return matchesSearch && matchesCategory;
  });
});

const goCriticalStock = () => router.push('/critical-stock');

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

const handleProductSaved = (saved) => {
  const exists = products.value.some(p => p.id === saved.id);
  products.value = exists ? products.value.map(p => (p.id === saved.id ? saved : p)) : [saved, ...products.value];
};

const handleDelete = async (product) => {
  if (!window.confirm(`¿Eliminar el producto ${product.sku} - ${product.name}?`)) return;
  try {
    await deleteProduct(product.id);
    products.value = products.value.filter(p => p.id !== product.id);
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo eliminar el producto.');
  }
};

const runExport = async (exportFn) => {
  try {
    await exportFn();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo generar el reporte.');
  }
};

const exportToExcel = () => runExport(downloadExcelReport);
const exportToPDF = () => runExport(downloadPdfReport);

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  router.push('/login');
};

onMounted(fetchProducts);
</script>
