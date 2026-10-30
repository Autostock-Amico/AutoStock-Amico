<template>
  <div style="padding: 2rem; font-family: sans-serif; max-width: 1200px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
      <div>
        <h1 style="color: #dc3545; margin: 0; display: flex; align-items: center; gap: 0.5rem;">
          ⚠️ Productos en Stock Crítico
        </h1>
        <p style="margin: 0.3rem 0 0 0; color: #6c757d;">Artículos con existencias menores o iguales a 5 unidades</p>
      </div>

      <div style="display: flex; gap: 0.5rem;">
        <button @click="goDashboard" style="padding: 0.5rem 1rem; background-color: #6c757d; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
          ← Volver al Catálogo
        </button>
      </div>
    </div>

    <!-- Indicador de Carga / Estado Vacío -->
    <div v-if="loading" style="text-align: center; padding: 2rem; color: #007bff; font-weight: bold;">
      Consultando alertas de inventario...
    </div>

    <div v-else-if="criticalProducts.length === 0" style="background: #d1e7dd; color: #0f5132; padding: 1.5rem; border-radius: 8px; text-align: center; font-weight: bold;">
      ✅ Todos los productos cuentan con stock suficiente. No hay alertas críticas.
    </div>

    <!-- Tabla con Filtro Crítico -->
    <ProductTable
      v-else
      :products="criticalProducts"
      @adjust-stock="openStockModal"
      @edit="openEditModal"
    />

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
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axiosClient from '../api/axiosClient';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import { getLocalProducts, saveLocalProducts } from '../services/storage';

const router = useRouter();
const criticalProducts = ref([]);
const loading = ref(true);

const isModalOpen = ref(false);
const editingProduct = ref(null);

const isStockModalOpen = ref(false);
const stockProduct = ref(null);

const fetchCriticalProducts = async () => {
  loading.value = true;
  try {
    const response = await axiosClient.get('/products/critical-stock');
    const data = Array.isArray(response.data) ? response.data : (response.data.products || []);
    criticalProducts.value = data.filter(p => (p.stock || 0) <= 5);
  } catch (err) {
    const allProducts = getLocalProducts();
    criticalProducts.value = allProducts.filter(p => (p.stock || 0) <= 5);
  } finally {
    loading.value = false;
  }
};

const goDashboard = () => {
  router.push('/dashboard');
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
  const allProducts = getLocalProducts();
  const targetId = savedProduct._id || savedProduct.id;
  const index = allProducts.findIndex(p => (p._id || p.id) === targetId);

  if (index !== -1) {
    allProducts[index] = { ...savedProduct };
  } else {
    allProducts.unshift(savedProduct);
  }
  saveLocalProducts(allProducts);
  fetchCriticalProducts();
};

const handleStockAdjusted = (updatedProduct) => {
  const allProducts = getLocalProducts();
  const targetId = updatedProduct._id || updatedProduct.id;
  const index = allProducts.findIndex(p => (p._id || p.id) === targetId);

  if (index !== -1) {
    allProducts[index].stock = updatedProduct.stock;
    saveLocalProducts(allProducts);
  }
  fetchCriticalProducts();
};

onMounted(() => {
  fetchCriticalProducts();
});
</script>
