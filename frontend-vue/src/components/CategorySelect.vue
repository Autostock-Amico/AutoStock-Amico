<template>
  <div>
    <select
      :value="isAdding ? NEW_OPTION : modelValue"
      @change="handleSelect($event.target.value)"
      required
      style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box; background: white;"
    >
      <option value="" disabled>Seleccioná una categoría</option>
      <option v-for="name in options" :key="name" :value="name">{{ name }}</option>
      <option :value="NEW_OPTION">+ Nueva categoría...</option>
    </select>

    <div v-if="isAdding" style="display: flex; gap: 0.5rem; margin-top: 0.5rem;">
      <input
        v-model="newName"
        type="text"
        placeholder="Nombre de la nueva categoría"
        @keydown.enter.prevent="addCategory"
        style="flex: 1; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
      />
      <button
        type="button"
        :disabled="saving"
        @click="addCategory"
        style="padding: 0.5rem 0.8rem; background: #198754; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"
      >
        {{ saving ? '...' : 'Agregar' }}
      </button>
      <button
        type="button"
        @click="cancelAdding"
        style="padding: 0.5rem 0.8rem; background: #6c757d; color: #fff; border: none; border-radius: 4px; cursor: pointer;"
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
  const all = [...savedCategories.value, ...props.extraOptions, props.modelValue];
  return [...new Set(all.filter(Boolean))].sort((a, b) => a.localeCompare(b, 'es'));
});

const loadCategories = async () => {
  try {
    const data = await getCategories();
    savedCategories.value = data.map(c => c.name);
  } catch (err) {
    error.value = getApiErrorMessage(err, 'No se pudieron cargar las categorías.');
  }
};

const handleSelect = (value) => {
  error.value = '';
  if (value === NEW_OPTION) {
    isAdding.value = true;
    return;
  }
  emit('update:modelValue', value);
};

const cancelAdding = () => {
  isAdding.value = false;
  newName.value = '';
  error.value = '';
};

const findExisting = (name) => options.value.find(o => o.toLowerCase() === name.toLowerCase());

const selectCategory = (name) => {
  emit('update:modelValue', name);
  cancelAdding();
};

const addCategory = async () => {
  const name = newName.value.trim();
  if (!name) {
    error.value = 'Escribí el nombre de la categoría.';
    return;
  }

  const existing = findExisting(name);
  if (existing) {
    selectCategory(existing);
    return;
  }

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

onMounted(loadCategories);
</script>
