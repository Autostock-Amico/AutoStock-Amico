<template>
  <div class="card row" style="margin-bottom: 1.5rem;">
    <div style="flex: 2;">
      <label class="form-label">Buscar (SKU / Nombre)</label>
      <input
        class="form-control"
        type="text"
        :value="search"
        placeholder="Ej: ART-001 o Aceite..."
        @input="$emit('update:search', $event.target.value)"
      />
    </div>
    <div>
      <label class="form-label">Categoría</label>
      <select class="form-control" :value="category" @change="$emit('update:category', $event.target.value)">
        <option value="">Todas las categorías</option>
        <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
      </select>
    </div>
  </div>
</template>

<script setup>
defineProps({
  search: { type: String, default: '' },
  category: { type: String, default: '' },
  categories: { type: Array, default: () => [] }
});

defineEmits(['update:search', 'update:category']);
</script>
