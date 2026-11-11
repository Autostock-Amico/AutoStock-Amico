<template>
  <div class="page-header">
    <h1 class="page-title">Catálogo de Productos</h1>
    <div class="toolbar">
      <button class="btn btn-success" @click="$emit('export-excel')">📊 Exportar a Excel</button>
      <button class="btn btn-primary" @click="$emit('export-pdf')">📄 Exportar a PDF</button>
      <button class="btn btn-danger" @click="$emit('critical-stock')">⚠️ Stock Crítico</button>
      <button class="btn btn-success" @click="$emit('create')">+ Nuevo Producto</button>
      <button class="btn btn-secondary" @click="$emit('logout')">Cerrar Sesión</button>
    </div>
  </div>
</template>

<script setup>
defineEmits(['export-excel', 'export-pdf', 'critical-stock', 'create', 'logout']);
</script>
