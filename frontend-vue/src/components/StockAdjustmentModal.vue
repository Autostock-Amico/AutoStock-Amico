<template>
  <BaseModal :isOpen="isOpen" title="Ajuste de Stock" @close="closeModal">
    <div v-if="product" class="product-info">
      <strong>{{ product.name }}</strong><br />
      <small>SKU: <strong>{{ product.sku }}</strong> | Stock Actual: <strong>{{ product.currentStock }} u.</strong></small>
    </div>

    <div v-if="errorMessage" class="alert alert-error">{{ errorMessage }}</div>

    <form @submit.prevent="handleSubmit">
      <FormField label="Tipo de Movimiento *">
        <MovementTypeToggle v-model="type" />
      </FormField>

      <FormField label="Cantidad *">
        <input v-model.number="quantity" class="form-control" type="number" min="1" max="10000" step="1" required placeholder="Ej: 5" />
      </FormField>

      <div class="form-actions">
        <button type="button" class="btn btn-secondary" @click="closeModal">Cancelar</button>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Procesando...' : 'Aplicar Ajuste' }}
        </button>
      </div>
    </form>
  </BaseModal>
</template>

<script setup>
import { ref, watch } from 'vue';
import BaseModal from './BaseModal.vue';
import FormField from './FormField.vue';
import MovementTypeToggle from './MovementTypeToggle.vue';
import { adjustStock, getApiErrorMessage } from '../services/productService';
import { validateStockMovement } from '../services/productForm';

const props = defineProps({
  isOpen: Boolean,
  product: Object
});

const emit = defineEmits(['close', 'adjusted']);

const type = ref('IN');
const quantity = ref(1);
const isSubmitting = ref(false);
const errorMessage = ref('');

const resetForm = () => {
  type.value = 'IN';
  quantity.value = 1;
  errorMessage.value = '';
};

watch(() => props.isOpen, (open) => open && resetForm());

const closeModal = () => {
  errorMessage.value = '';
  emit('close');
};

const handleSubmit = async () => {
  const qty = Number(quantity.value);
  errorMessage.value = validateStockMovement(type.value, qty, Number(props.product.currentStock));
  if (errorMessage.value) return;

  isSubmitting.value = true;
  try {
    emit('adjusted', await adjustStock(props.product.id, type.value, qty));
    closeModal();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo ajustar el stock.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>
