<template>
  <div class="page">
    <ProductsToolbar
      @export-excel="runExport(downloadExcelReport, 'Excel')"
      @export-pdf="runExport(downloadPdfReport, 'PDF')"
      @create="openProductModal(null)"
    />

    <InventoryStats v-if="!loading" :products="products" />

    <ProductFilters v-model:search="searchQuery" v-model:category="selectedCategory" :categories="categories" />

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>
    <div v-if="loading" class="loading"><div class="spinner"></div>Cargando catálogo...</div>

    <ProductTable
      v-else
      :products="filteredProducts"
      @edit="openProductModal"
      @adjust-stock="openStockModal"
      @delete="handleDelete"
    />

    <ProductFormModal
      :isOpen="isModalOpen"
      :productToEdit="editingProduct"
      :categories="categories"
      @close="isModalOpen = false"
      @saved="handleSaved"
    />

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
import ProductsToolbar from '../components/ProductsToolbar.vue';
import InventoryStats from '../components/InventoryStats.vue';
import ProductFilters from '../components/ProductFilters.vue';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import { useProducts } from '../composables/useProducts';
import { useToast } from '../composables/useToast';
import { downloadExcelReport, downloadPdfReport } from '../services/productService';

const {
  products, searchQuery, selectedCategory, loading, errorMessage, categories, filteredProducts,
  fetchProducts, upsertProduct, removeProduct, runExport
} = useProducts();
const toast = useToast();

const isModalOpen = ref(false);
const editingProduct = ref(null);
const isStockModalOpen = ref(false);
const stockProduct = ref(null);

const openProductModal = (product) => {
  editingProduct.value = product;
  isModalOpen.value = true;
};

const openStockModal = (product) => {
  stockProduct.value = product;
  isStockModalOpen.value = true;
};

const handleSaved = (product) => {
  const wasEdited = upsertProduct(product);
  toast.success(wasEdited ? `Producto ${product.sku} actualizado` : `Producto ${product.sku} creado`);
};

const handleStockAdjusted = (product) => {
  upsertProduct(product);
  toast.success(`Stock de ${product.sku} actualizado: ${product.currentStock} u.`);
};

const handleDelete = (product) => {
  if (window.confirm(`¿Eliminar el producto ${product.sku} - ${product.name}?`)) removeProduct(product);
};

onMounted(fetchProducts);
</script>