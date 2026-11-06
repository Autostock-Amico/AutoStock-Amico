<template>
  <div style="border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; background: white;">
    <table style="width: 100%; border-collapse: collapse; text-align: left;">
      <thead>
        <tr style="background: #f8f9fa; border-bottom: 2px solid #dee2e6;">
          <th style="padding: 0.75rem 1rem;">SKU</th>
          <th style="padding: 0.75rem 1rem;">Nombre</th>
          <th style="padding: 0.75rem 1rem;">Categoría</th>
          <th style="padding: 0.75rem 1rem; text-align: right;">Precio Venta</th>
          <th style="padding: 0.75rem 1rem; text-align: center;">Stock Actual</th>
          <th style="padding: 0.75rem 1rem; text-align: center;">Acciones</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in products" :key="p.sku || p.id" style="border-bottom: 1px solid #dee2e6;">
          <td style="padding: 0.75rem 1rem; font-weight: bold;">{{ p.sku || 'N/A' }}</td>
          <td style="padding: 0.75rem 1rem;">
            {{ p.name || p.nombre }}
            <span v-if="Number(p.stock) <= 5" style="background-color: #dc3545; color: white; padding: 0.15rem 0.4rem; border-radius: 4px; font-size: 0.75rem; margin-left: 0.5rem; font-weight: bold;">
              CRÍTICO
            </span>
          </td>
          <td style="padding: 0.75rem 1rem;">
            <span style="background: #e9ecef; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.85rem;">
              {{ p.category || p.categoria || 'General' }}
            </span>
          </td>
          <td style="padding: 0.75rem 1rem; text-align: right; color: #198754; font-weight: bold;">
            $ {{ Number(p.price || p.precio || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }) }}
          </td>
          <td style="padding: 0.75rem 1rem; text-align: center;">
            <span :style="{ backgroundColor: Number(p.stock) <= 5 ? '#dc3545' : '#198754', color: 'white', padding: '0.25rem 0.6rem', borderRadius: '12px', fontWeight: 'bold', fontSize: '0.85rem' }">
              {{ p.stock }} u.
            </span>
          </td>
          <td style="padding: 0.75rem 1rem; text-align: center;">
            <button @click="$emit('adjust-stock', p)" style="background: #0d6efd; color: white; border: none; padding: 0.35rem 0.7rem; border-radius: 4px; margin-right: 0.3rem; cursor: pointer; font-weight: bold;">Stock</button>
            <button @click="$emit('edit-product', p)" style="background: #ffc107; color: #212529; border: none; padding: 0.35rem 0.7rem; border-radius: 4px; cursor: pointer; font-weight: bold;">Editar</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  products: {
    type: Array,
    required: true
  }
});

defineEmits(['adjust-stock', 'edit-product']);
</script>