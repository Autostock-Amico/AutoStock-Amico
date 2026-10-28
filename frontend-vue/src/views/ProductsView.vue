<template>
  <div style="padding: 2rem; font-family: sans-serif; max-width: 1200px; margin: 0 auto;">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
      <h1 style="color: #333; margin: 0;">Catálogo de Productos</h1>
      <div style="display: flex; gap: 0.5rem;">
        <button @click="openCreateModal" style="padding: 0.5rem 1rem; background-color: #198754; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
          + Nuevo Producto
        </button>
        <button @click="handleLogout" style="padding: 0.5rem 1rem; background-color: #dc3545; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
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
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axiosClient from '../api/axiosClient';
import ProductTable from '../components/ProductTable.vue';
import ProductFormModal from '../components/ProductFormModal.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';

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
    } else if (products.value.length === 0) {
      loadMockData();
    }
  } catch (err) {
    if (products.value.length === 0) {
      loadMockData();
    }
  } finally {
    loading.value = false;
  }
};

const loadMockData = () => {
  products.value = [
    { id: '1', sku: 'FLT-001', name: 'Filtro de Aceite', category: 'Filtros', price: 4500, stock: 12 },
    { id: '2', sku: 'FLT-002', name: 'Filtro de Aire', category: 'Filtros', price: 6200, stock: 3 },
    { id: '3', sku: 'ACE-010', name: 'Aceite Sintético 5W30', category: 'Lubricantes', price: 28500, stock: 8 },
    { id: '4', sku: 'PST-005', name: 'Pastillas de Freno Delanteras', category: 'Frenos', price: 18900, stock: 2 }
  ];
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
};

const handleStockAdjusted = (updatedProduct) => {
  const targetId = updatedProduct._id || updatedProduct.id;
  const index = products.value.findIndex(p => (p._id || p.id) === targetId);

  if (index !== -1) {
    products.value[index] = { ...products.value[index], stock: updatedProduct.stock };
    products.value = [...products.value];
  }
};

const handleLogout = () => {
  localStorage.removeItem('token');
  router.push('/login');
};

onMounted(() => {
  fetchProducts();
});
</script>
