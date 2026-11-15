<template>
  <div class="page">
    <div class="page-header">
      <div>
        <h1 class="page-title">⚠️ Productos en Stock Crítico</h1>
        <p class="page-subtitle">Artículos con stock actual menor o igual a su stock mínimo.</p>
      </div>
    </div>

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>
    <div v-if="loading" class="loading"><div class="spinner"></div>Cargando...</div>

    <div v-else-if="criticalProducts.length === 0" class="alert alert-ok">
      ✅ Todos los productos cuentan con niveles de stock adecuados.
    </div>

    <template v-else>
      <div class="critical-banner">
        <span class="banner-icon">🚨</span>
        <div>
          <strong>{{ criticalProducts.length }} producto(s) necesitan reposición</strong>
          <p>Faltan {{ totalMissing }} unidades en total para llegar a los mínimos configurados.</p>
        </div>
      </div>

      <CriticalStockTable :products="criticalProducts" @restock="openRestock" />
    </template>

    <StockAdjustmentModal
      :isOpen="isStockModalOpen"
      :product="stockProduct"
      @close="isStockModalOpen = false"
      @adjusted="handleRestocked"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import CriticalStockTable from '../components/CriticalStockTable.vue';
import StockAdjustmentModal from '../components/StockAdjustmentModal.vue';
import { useToast } from '../composables/useToast';
import { getCriticalStock, getApiErrorMessage, isCritical, missingUnits } from '../services/productService';

const toast = useToast();
const criticalProducts = ref([]);
const loading = ref(true);
const errorMessage = ref('');
const isStockModalOpen = ref(false);
const stockProduct = ref(null);

const totalMissing = computed(() => criticalProducts.value.reduce((acc, p) => acc + missingUnits(p), 0));

const loadCriticalStock = async () => {
  try {
    criticalProducts.value = await getCriticalStock();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo cargar el stock crítico.');
  } finally {
    loading.value = false;
  }
};

const openRestock = (product) => {
  stockProduct.value = product;
  isStockModalOpen.value = true;
};

const handleRestocked = (updated) => {
  criticalProducts.value = criticalProducts.value
    .map(p => (p.id === updated.id ? updated : p))
    .filter(isCritical);
  toast.success(`Stock de ${updated.sku} actualizado: ${updated.currentStock} u.`);
};

onMounted(loadCriticalStock);
</script>