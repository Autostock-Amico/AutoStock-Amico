<template>
  <div class="page-header">
    <div>
      <h1 class="page-title">Catálogo de Productos</h1>
      <p class="page-subtitle">Gestioná tu inventario, stock y reportes.</p>
    </div>
    <div class="toolbar">
      <ExportMenu @export-excel="$emit('export-excel')" @export-pdf="$emit('export-pdf')" />
      <button class="btn btn-primary" @click="$emit('create')">+ Nuevo producto</button>
    </div>
  </div>
</template>

<script setup>
import ExportMenu from './ExportMenu.vue';

defineEmits(['export-excel', 'export-pdf', 'create']);
</script>