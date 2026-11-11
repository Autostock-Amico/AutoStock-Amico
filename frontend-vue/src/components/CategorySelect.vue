<template>
  <div>
    <select
      :value="isAdding ? NEW_OPTION : modelValue"
      @change="handleSelect($event.target.value)"
      class="form-control"
      required
    >
      <option value="" disabled>Seleccioná una categoría</option>
      <option v-for="name in options" :key="name" :value="name">{{ name }}</option>
      <option :value="NEW_OPTION">+ Nueva categoría...</option>
    </select>

    <div v-if="isAdding" class="toolbar" style="margin-top: 0.5rem; flex-wrap: nowrap;">
      <input
        v-model="newName"
        type="text"
        placeholder="Nombre de la nueva categoría"
        class="form-control"
        @keydown.enter.prevent="addCategory"
      />
      <button
        type="button"
        :disabled="saving"
        class="btn btn-success"
        @click="addCategory"
      >
        {{ saving ? '...' : 'Agregar' }}
      </button>
      <button
        type="button"
        class="btn btn-secondary"
        @click="cancelAdding"
      >
        ✕
      </button>
    </div>

    <div v-if="error" style="color: #721c24; font-size: 0.85rem; margin-top: 0.3rem;">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { getCategories, createCategory } from '../services/categoryService';
import { getApiErrorMessage } from '../services/productService';

const props = defineProps({
  modelValue: { type: String, default: '' },
  extraOptions: { type: Array, default: () => [] }
});

const emit = defineEmits(['update:modelValue']);

const NEW_OPTION = '__nueva__';

const savedCategories = ref([]);
const isAdding = ref(false);
const newName = ref('');
const saving = ref(false);
const error = ref('');

const options = computed(() => {
  const all = [...savedCategories.value, ...props.extraOptions, props.modelValue].filter(Boolean);
  return [...new Set(all)].sort((a, b) => a.localeCompare(b, 'es'));
});

const handleSelect = (value) => {
  error.value = '';
  if (value === NEW_OPTION) isAdding.value = true;
  else emit('update:modelValue', value);
};

const cancelAdding = () => {
  isAdding.value = false;
  newName.value = '';
  error.value = '';
};

const selectCategory = (name) => {
  emit('update:modelValue', name);
  cancelAdding();
};

const saveNewCategory = async (name) => {
  saving.value = true;
  try {
    const created = await createCategory(name);
    savedCategories.value = [...savedCategories.value, created.name];
    selectCategory(created.name);
  } catch (err) {
    error.value = getApiErrorMessage(err, 'No se pudo crear la categoría.');
  } finally {
    saving.value = false;
  }
};

const addCategory = () => {
  const name = newName.value.trim();
  if (!name) {
    error.value = 'Escribí el nombre de la categoría.';
    return;
  }
  const existing = options.value.find(o => o.toLowerCase() === name.toLowerCase());
  if (existing) selectCategory(existing);
  else saveNewCategory(name);
};

onMounted(async () => {
  try {
    savedCategories.value = (await getCategories()).map(c => c.name);
  } catch (err) {
    error.value = getApiErrorMessage(err, 'No se pudieron cargar las categorías.');
  }
});
</script>
