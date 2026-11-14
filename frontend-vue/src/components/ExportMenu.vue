<template>
  <div class="dropdown" @mouseleave="open = false">
    <button class="btn btn-secondary" @click="open = !open">⬇️ Exportar ▾</button>
    <div v-if="open" class="dropdown-menu">
      <button class="dropdown-item" @click="select('export-excel')">📊 Excel (.xlsx)</button>
      <button class="dropdown-item" @click="select('export-pdf')">📄 PDF</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const emit = defineEmits(['export-excel', 'export-pdf']);
const open = ref(false);

const select = (eventName) => {
  open.value = false;
  emit(eventName);
};
</script>