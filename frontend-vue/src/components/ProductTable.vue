<template>
  <div class="table-wrapper">
    <table class="table">
      <thead>
        <tr>
          <th>SKU</th>
          <th>Nombre</th>
          <th>Categoría</th>
          <th>Precio Venta</th>
          <th>Stock Actual</th>
          <th class="center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="products.length === 0">
          <td colspan="6" class="center" style="color: #6c757d;">No se encontraron productos en la lista.</td>
        </tr>
        <tr v-for="product in products" :key="product.id" :class="{ 'row-critical': isCritical(product) }">
          <td><strong>{{ product.sku }}</strong></td>
          <td>
            {{ product.name }}
            <span v-if="isCritical(product)" class="badge badge-danger" style="margin-left: 8px; font-size: 0.7rem;">CRÍTICO</span>
          </td>
          <td><span class="badge badge-muted">{{ product.category || 'Sin Categoría' }}</span></td>
          <td style="color: #28a745; font-weight: bold;">${{ formatMoney(product.salePrice) }}</td>
          <td>
            <span class="badge" :class="isCritical(product) ? 'badge-danger' : 'badge-success'">
              {{ product.currentStock }} u. <small style="opacity: 0.8;">(mín. {{ product.minStock }})</small>
            </span>
          </td>
          <td class="center">
            <div class="toolbar" style="justify-content: center;">
              <button class="btn btn-primary btn-sm" @click="$emit('adjust-stock', product)">Stock</button>
              <button class="btn btn-warning btn-sm" @click="$emit('edit', product)">Editar</button>
              <button class="btn btn-danger btn-sm" @click="$emit('delete', product)">Eliminar</button>
            </div>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { isCritical, formatMoney } from '../services/productService';

defineProps({
  products: { type: Array, required: true }
});

defineEmits(['edit', 'adjust-stock', 'delete']);
</script>
