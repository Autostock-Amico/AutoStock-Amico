<template>
  <BaseModal :isOpen="isOpen" :title="isEditing ? 'Editar Producto' : 'Nuevo Producto'" @close="closeModal">
    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>

    <form @submit.prevent="handleSubmit">
      <FormField label="SKU * (Ej: ART-001)">
        <input
          v-model="form.sku"
          class="form-control"
          type="text"
          required
          placeholder="Ej: ART-001"
          @input="form.sku = form.sku.toUpperCase()"
        />
      </FormField>

      <FormField label="Nombre *">
        <input v-model="form.name" class="form-control" type="text" required placeholder="Ej: Filtro de Aceite" />
      </FormField>

      <FormField label="Categoría *">
        <CategorySelect v-model="form.category" :extra-options="categories" />
      </FormField>

      <div v-for="(pair, index) in NUMBER_ROWS" :key="index" class="row">
        <FormField v-for="field in pair" :key="field.key" :label="field.label">
          <input v-model.number="form[field.key]" class="form-control" type="number" min="0" :step="field.step" required />
        </FormField>
      </div>

      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear Producto') }}
        </button>
      </div>
    </form>
  </BaseModal>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import BaseModal from './BaseModal.vue';
import FormField from './FormField.vue';
import CategorySelect from './CategorySelect.vue';
import { createProduct, updateProduct, getApiErrorMessage } from '../services/productService';
import { EMPTY_PRODUCT, toProductForm, validateProduct } from '../services/productForm';

const props = defineProps({
  isOpen: Boolean,
  productToEdit: Object,
  categories: { type: Array, default: () => [] }
});

const emit = defineEmits(['close', 'saved']);

const NUMBER_ROWS = [
  [{ key: 'costPrice', label: 'Precio Costo ($) *', step: '0.01' }, { key: 'salePrice', label: 'Precio Venta ($) *', step: '0.01' }],
  [{ key: 'currentStock', label: 'Stock Actual (Máx 10.000) *', step: '1' }, { key: 'minStock', label: 'Stock Mínimo *', step: '1' }]
];

const isSubmitting = ref(false);
const errorMessage = ref('');
const form = ref({ ...EMPTY_PRODUCT });

const isEditing = computed(() => !!props.productToEdit?.id);

const fillForm = (product) => {
  form.value = toProductForm(product);
  errorMessage.value = '';
};

watch(() => props.productToEdit, fillForm, { immediate: true });

const closeModal = () => {
  fillForm(null);
  emit('close');
};

const saveProduct = (data) =>
  isEditing.value ? updateProduct(props.productToEdit.id, data) : createProduct(data);

const handleSubmit = async () => {
  const data = { ...form.value, sku: form.value.sku.trim().toUpperCase() };
  errorMessage.value = validateProduct(data);
  if (errorMessage.value) return;

  isSubmitting.value = true;
  try {
    emit('saved', await saveProduct(data));
    closeModal();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo guardar el producto.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>
