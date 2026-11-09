<template>
  <div style="padding: 2rem; font-family: sans-serif; max-width: 1200px; margin: 0 auto;">
    <!-- Header -->
    <div style="margin-bottom: 1.5rem;">
      <button @click="goBack" style="background: transparent; border: none; color: #0d6efd; cursor: pointer; padding: 0; margin-bottom: 0.5rem; font-weight: bold;">← Volver al catálogo</button>
      <h1 style="color: #dc3545; margin: 0;">Productos en Stock Crítico</h1>
      <p style="color: #6c757d; margin: 0.3rem 0 0 0;">Artículos con stock actual menor o igual a su stock mínimo.</p>
    </div>

    <div v-if="errorMessage" style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 4px; margin-bottom: 1rem;">
      {{ errorMessage }}
    </div>

    <div v-if="loading" style="text-align: center; padding: 2rem; color: #007bff; font-weight: bold;">
      Cargando...
    </div>

    <div v-else-if="criticalProducts.length === 0" style="padding: 1.5rem; background: #e8f5e9; color: #2e7d32; border-radius: 6px; font-weight: bold; text-align: center;">
      Todos los productos cuentan con niveles de stock adecuados.
    </div>

    <!-- Tabla -->
    <div v-else style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; background: white;">
      <table style="width: 100%; border-collapse: collapse; text-align: left;">
        <thead>
          <tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">
            <th style="padding: 0.75rem 1rem;">SKU</th>
            <th style="padding: 0.75rem 1rem;">Producto</th>
            <th style="padding: 0.75rem 1rem;">Categoría</th>
            <th style="padding: 0.75rem 1rem; text-align: right;">Precio Venta</th>
            <th style="padding: 0.75rem 1rem; text-align: center;">Stock</th>
            <th style="padding: 0.75rem 1rem; text-align: center;">Mínimo</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="p in criticalProducts" :key="p.id" style="border-bottom: 1px solid #dee2e6;">
            <td style="padding: 0.75rem 1rem; font-weight: bold;">{{ p.sku }}</td>
            <td style="padding: 0.75rem 1rem;">{{ p.name }}</td>
            <td style="padding: 0.75rem 1rem;">{{ p.category }}</td>
            <td style="padding: 0.75rem 1rem; text-align: right;">$ {{ Number(p.salePrice || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }) }}</td>
            <td style="padding: 0.75rem 1rem; text-align: center;">
              <span style="background-color: #dc3545; color: white; padding: 0.25rem 0.6rem; border-radius: 12px; font-weight: bold; font-size: 0.85rem;">
                {{ p.currentStock }} u.
              </span>
            </td>
            <td style="padding: 0.75rem 1rem; text-align: center;">{{ p.minStock }} u.</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getCriticalStock, getApiErrorMessage } from '../services/productService';

const router = useRouter();
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

const goBack = () => router.push('/dashboard');

onMounted(loadCriticalStock);
</script>
