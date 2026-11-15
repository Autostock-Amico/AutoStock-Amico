<template>
  <div class="table-wrapper">
    <table class="table">
      <thead>
        <tr>
          <th>SKU</th>
          <th>Producto</th>
          <th>Categoría</th>
          <th class="center">Stock</th>
          <th class="center">Mínimo</th>
          <th class="center">Faltan</th>
          <th class="center">Acción</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in products" :key="p.id" class="row-critical">
          <td><span class="sku">{{ p.sku }}</span></td>
          <td>{{ p.name }}</td>
          <td><span class="badge badge-muted">{{ p.category }}</span></td>
          <td class="center"><span class="badge badge-danger">{{ p.currentStock }} u.</span></td>
          <td class="center">{{ p.minStock }} u.</td>
          <td class="center">
            <span v-if="missingUnits(p) > 0" class="missing">{{ missingUnits(p) }} u.</span>
            <small v-else>En el límite</small>
          </td>
          <td class="center">
            <button class="btn btn-primary btn-sm" @click="$emit('restock', p)">+ Reponer</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { missingUnits } from '../services/productService';

defineProps({
  products: { type: Array, required: true }
});

defineEmits(['restock']);
</script>