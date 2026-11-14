<template>
  <div class="table-wrapper">
    <div v-if="products.length === 0" class="empty-state">
      <div class="empty-icon">🔍</div>
      <div>No se encontraron productos.</div>
      <small>Probá con otra búsqueda o creá un producto nuevo.</small>
    </div>

    <table v-else class="table">
      <thead>
        <tr>
          <th>SKU</th>
          <th>Producto</th>
          <th>Categoría</th>
          <th class="right">Precio venta</th>
          <th>Stock</th>
          <th class="center">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="product in products" :key="product.id" :class="{ 'row-critical': isCritical(product) }">
          <td><span class="sku">{{ product.sku }}</span></td>
          <td>
            {{ product.name }}
            <span v-if="isCritical(product)" class="badge badge-danger" style="margin-left: 6px;">Crítico</span>
          </td>
          <td><span class="badge badge-muted">{{ product.category || 'Sin categoría' }}</span></td>
          <td class="right text-money">${{ formatMoney(product.salePrice) }}</td>
          <td>
            <div class="stock-cell">
              <span class="badge" :class="isCritical(product) ? 'badge-danger' : 'badge-success'">{{ product.currentStock }} u.</span>
              <small>mín. {{ product.minStock }}</small>
            </div>
          </td>
          <td class="center">
            <div class="toolbar" style="justify-content: center;">
              <button class="btn btn-info btn-sm" title="Ajustar stock" @click="$emit('adjust-stock', product)">± Stock</button>
              <button class="btn btn-warning btn-sm icon-btn" title="Editar" @click="$emit('edit', product)">✏️</button>
              <button class="btn btn-danger btn-sm icon-btn" title="Eliminar" @click="$emit('delete', product)">🗑️</button>
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