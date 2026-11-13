<template>
  <div class="page-header">
    <div>
      <h1 class="page-title">Catálogo de Productos</h1>
      <p class="page-subtitle">Gestioná tu inventario, stock y reportes.</p>
    </div>
    <div class="toolbar">
      <button class="btn btn-secondary" @click="$emit('export-excel')">📊 Excel</button>
      <button class="btn btn-secondary" @click="$emit('export-pdf')">📄 PDF</button>
      <button class="btn btn-primary" @click="$emit('create')">+ Nuevo producto</button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['export-excel', 'export-pdf', 'create']);
</script>