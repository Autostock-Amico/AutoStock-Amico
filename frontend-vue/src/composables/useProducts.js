import { ref, computed } from 'vue';
import { getProducts, deleteProduct, getApiErrorMessage } from '../services/productService';

// Estado y operaciones del catálogo de productos
export function useProducts() {
  const products = ref([]);
  const searchQuery = ref('');
  const selectedCategory = ref('');
  const loading = ref(true);
  const errorMessage = ref('');

  const categories = computed(() => [...new Set(products.value.map(p => p.category).filter(Boolean))]);

  const matchesFilters = (p, query) =>
    (p.name.toLowerCase().includes(query) || p.sku.toLowerCase().includes(query)) &&
    (!selectedCategory.value || p.category === selectedCategory.value);

  const filteredProducts = computed(() => {
    const query = searchQuery.value.toLowerCase();
    return products.value.filter(p => matchesFilters(p, query));
  });

  const fetchProducts = async () => {
    try {
      products.value = await getProducts();
    } catch (err) {
      errorMessage.value = getApiErrorMessage(err, 'No se pudieron cargar los productos.');
    } finally {
      loading.value = false;
    }
  };

  const upsertProduct = (saved) => {
    const exists = products.value.some(p => p.id === saved.id);
    products.value = exists ? products.value.map(p => (p.id === saved.id ? saved : p)) : [saved, ...products.value];
  };

  const removeProduct = async (product) => {
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

  return {
    products, searchQuery, selectedCategory, loading, errorMessage, categories, filteredProducts,
    fetchProducts, upsertProduct, removeProduct, runExport
  };
}