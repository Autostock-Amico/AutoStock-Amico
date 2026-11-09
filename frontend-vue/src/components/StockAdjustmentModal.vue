<template>
  <div v-if="isOpen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
    <div style="background: white; border-radius: 8px; width: 90%; max-width: 450px; padding: 2rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2 style="margin: 0; color: #333; font-size: 1.3rem;">Ajuste de Stock</h2>
        <button @click="closeModal" style="background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #6c757d;">&times;</button>
      </div>

      <div v-if="product" style="background: #f8f9fa; padding: 0.75rem; border-radius: 6px; margin-bottom: 1.2rem; border-left: 4px solid #0d6efd;">
        <div style="font-weight: bold; color: #212529;">{{ product.name }}</div>
        <div style="font-size: 0.85rem; color: #6c757d;">
          SKU: <strong>{{ product.sku }}</strong> | Stock Actual: <strong>{{ product.currentStock }} u.</strong>
        </div>
      </div>

      <div v-if="errorMessage" style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit">
        <div style="margin-bottom: 1.2rem;">
          <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.4rem;">Tipo de Movimiento *</label>
          <div style="display: flex; gap: 0.5rem;">
            <button
              type="button"
              @click="type = 'IN'"
              :style="{
                flex: 1,
                padding: '0.6rem',
                borderRadius: '4px',
                border: '1px solid #198754',
                fontWeight: 'bold',
                cursor: 'pointer',
                backgroundColor: type === 'IN' ? '#198754' : '#fff',
                color: type === 'IN' ? '#fff' : '#198754'
              }"
            >
              + Entrada (Ingreso)
            </button>
            <button
              type="button"
              @click="type = 'OUT'"
              :style="{
                flex: 1,
                padding: '0.6rem',
                borderRadius: '4px',
                border: '1px solid #dc3545',
                fontWeight: 'bold',
                cursor: 'pointer',
                backgroundColor: type === 'OUT' ? '#dc3545' : '#fff',
                color: type === 'OUT' ? '#fff' : '#dc3545'
              }"
            >
              - Salida (Egreso)
            </button>
          </div>
        </div>

        <div style="margin-bottom: 1.5rem;">
          <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Cantidad *</label>
          <input
            v-model.number="quantity"
            type="number"
            min="1"
            max="10000"
            step="1"
            required
            placeholder="Ej: 5"
            style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box; font-size: 1rem;"
          />
        </div>

        <div style="display: flex; justify-content: flex-end; gap: 0.5rem;">
          <button
            type="button"
            @click="closeModal"
            style="padding: 0.5rem 1rem; background: #6c757d; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"
          >
            Cancelar
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            style="padding: 0.5rem 1rem; background: #0d6efd; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"
          >
            {{ isSubmitting ? 'Procesando...' : 'Aplicar Ajuste' }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import { adjustStock, getApiErrorMessage } from '../services/productService';

const props = defineProps({
  isOpen: Boolean,
  product: Object
});

const emit = defineEmits(['close', 'adjusted']);

const MAX_STOCK = 10000;

const type = ref('IN');
const quantity = ref(1);
const isSubmitting = ref(false);
const errorMessage = ref('');

watch(() => props.isOpen, (open) => {
  if (!open) return;
  type.value = 'IN';
  quantity.value = 1;
  errorMessage.value = '';
});

const closeModal = () => {
  errorMessage.value = '';
  emit('close');
};

const validate = (qty, current) => {
  if (!Number.isInteger(qty) || qty <= 0) return 'La cantidad debe ser un número entero mayor a 0.';
  if (type.value === 'OUT' && qty > current) {
    return `Stock insuficiente. Intenta retirar ${qty} u. pero solo hay ${current} u. disponibles.`;
  }
  if (type.value === 'IN' && current + qty > MAX_STOCK) {
    return `No se puede superar el stock máximo permitido de 10.000 unidades. (Stock actual: ${current} u.)`;
  }
  return '';
};

const handleSubmit = async () => {
  const qty = Number(quantity.value);
  errorMessage.value = validate(qty, Number(props.product.currentStock));
  if (errorMessage.value) return;

  isSubmitting.value = true;
  try {
    const updated = await adjustStock(props.product.id, type.value, qty);
    emit('adjusted', updated);
    closeModal();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo ajustar el stock.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>
