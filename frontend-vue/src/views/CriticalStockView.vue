<template>
  <div class="page">
    <div style="margin-bottom: 1.5rem;">
      <h1 class="page-title">⚠️ Productos en Stock Crítico</h1>
      <p class="page-subtitle">Artículos con stock actual menor o igual a su stock mínimo.</p>
    </div>

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>
    <div v-if="loading" class="loading">Cargando...</div>
    <div v-else-if="criticalProducts.length === 0" class="alert alert-ok">
      Todos los productos cuentan con niveles de stock adecuados.
    </div>

    <div v-else class="table-wrapper">
      <table class="table">
        <thead>
          <tr>
            <th>SKU</th>
            <th>Producto</th>
            <th>Categoría</th>
            <th class="right">Precio Venta</th>
            <th class="center">Stock</th>
            <th class="center">Mínimo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in criticalProducts" :key="p.id">
            <td><strong>{{ p.sku }}</strong></td>
            <td>{{ p.name }}</td>
            <td>{{ p.category }}</td>
            <td class="right">$ {{ formatMoney(p.salePrice) }}</td>
            <td class="center"><span class="badge badge-danger">{{ p.currentStock }} u.</span></td>
            <td class="center">{{ p.minStock }} u.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getCriticalStock, getApiErrorMessage, formatMoney } from '../services/productService';

const criticalProducts = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const loadCriticalStock = async () => {
  try {
    criticalProducts.value = await getCriticalStock();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo cargar el stock crítico.');
  } finally {
    loading.value = false;
  }
};

onMounted(loadCriticalStock);
</script>
