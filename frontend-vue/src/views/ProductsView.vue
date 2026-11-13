<template>
  <div class="page">
    <ProductsToolbar
      @export-excel="runExport(downloadExcelReport)"
      @export-pdf="runExport(downloadPdfReport)"
      @create="openProductModal(null)"
    />

    <ProductFilters v-model:search="searchQuery" v-model:category="selectedCategory" :categories="categories" />

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>
    <div v-if="loading" class="loading">Cargando catálogo...</div>

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
      @saved="upsertProduct"
    />

    <StockAdjustmentModal
      :isOpen="isStockModalOpen"
      :product="stockProduct"
      @close="isStockModalOpen = false"
      @adjusted="upsertProduct"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import ProductsToolbar from '../components/ProductsToolbar.vue';
import ProductFilters from '../components/ProductFilters.vue';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import { useProducts } from '../composables/useProducts';
import { downloadExcelReport, downloadPdfReport } from '../services/productService';

const {
  searchQuery, selectedCategory, loading, errorMessage, categories, filteredProducts,
  fetchProducts, upsertProduct, removeProduct, runExport
} = useProducts();

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

const handleDelete = (product) => {
  if (window.confirm(`¿Eliminar el producto ${product.sku} - ${product.name}?`)) removeProduct(product);
};

onMounted(fetchProducts);
</script>
