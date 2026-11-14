<template>
  <div class="stats-grid">
    <div v-for="stat in stats" :key="stat.label" class="stat-card" :class="stat.variant">
      <span class="stat-icon">{{ stat.icon }}</span>
      <div>
        <div class="stat-label">{{ stat.label }}</div>
        <div class="stat-value">{{ stat.value }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { isCritical, formatMoney } from '../services/productService';

const props = defineProps({
  products: { type: Array, required: true }
});

const sumBy = (field) =>
  props.products.reduce((acc, p) => acc + Number(p[field] || 0) * Number(p.currentStock || 0), 0);

const stats = computed(() => [
  { label: 'Productos', value: props.products.length, icon: '📦', variant: 'is-info' },
  { label: 'En stock crítico', value: props.products.filter(isCritical).length, icon: '⚠️', variant: 'is-danger' },
  { label: 'Valorización a costo', value: `$${formatMoney(sumBy('costPrice'))}`, icon: '💰', variant: '' },
  { label: 'Valorización a venta', value: `$${formatMoney(sumBy('salePrice'))}`, icon: '📈', variant: 'is-success' }
]);
</script>