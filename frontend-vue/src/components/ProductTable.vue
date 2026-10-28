<template>
  <div style="overflow-x: auto;">
    <table style="width: 100%; border-collapse: collapse; background: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
      <thead>
        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6; text-align: left;">
          <th style="padding: 12px;">SKU</th>
          <th style="padding: 12px;">Nombre</th>
          <th style="padding: 12px;">Categoría</th>
          <th style="padding: 12px;">Precio Venta</th>
          <th style="padding: 12px;">Stock Actual</th>
        </tr>
      </thead>
      <tbody>
        <tr v-if="products.length === 0">
          <td colspan="5" style="text-align: center; padding: 20px; color: #6c757d;">
            No se encontraron productos que coincidan con la búsqueda.
          </td>
        </tr>
        <tr v-for="product in products" :key="product._id || product.id || product.sku" style="border-bottom: 1px solid #e9ecef;">
          <td style="padding: 12px; font-weight: bold; color: #495057;">{{ product.sku }}</td>
          <td style="padding: 12px;">{{ product.name || product.nombre }}</td>
          <td style="padding: 12px;">
            <span style="background: #e9ecef; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem;">
              {{ product.category || product.categoria || 'Sin Categoría' }}
            </span>
          </td>
          <td style="padding: 12px; color: #28a745; font-weight: bold;">
            ${{ Number(product.price || product.precio || 0).toLocaleString('es-AR', { minimumFractionDigits: 2 }) }}
          </td>
          <td style="padding: 12px;">
            <span :style="{
              padding: '4px 8px',
              borderRadius: '4px',
              fontWeight: 'bold',
              fontSize: '0.85rem',
              color: '#fff',
              backgroundColor: (product.stock || 0) <= 5 ? '#dc3545' : '#198754'
            }">
              {{ product.stock || 0 }} u.
            </span>
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
</script>
