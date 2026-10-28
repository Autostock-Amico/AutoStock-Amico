<template>
  <div v-if="isOpen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
    <div style="background: white; border-radius: 8px; width: 90%; max-width: 450px; padding: 2rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
        <h2 style="margin: 0; color: #333; font-size: 1.3rem;">Ajuste de Stock</h2>
        <button @click="closeModal" style="background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #6c757d;">&times;</button>
      </div>

      <div v-if="product" style="background: #f8f9fa; padding: 0.75rem; border-radius: 6px; margin-bottom: 1.2rem; border-left: 4px solid #0d6efd;">
        <div style="font-weight: bold; color: #212529;">{{ product.name || product.nombre }}</div>
        <div style="font-size: 0.85rem; color: #6c757d;">
          SKU: <strong>{{ product.sku }}</strong> | Stock Actual: <strong>{{ product.stock || 0 }} u.</strong>
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
import axiosClient from '../api/axiosClient';

const props = defineProps({
  isOpen: Boolean,
  product: Object
});

const emit = defineEmits(['close', 'adjusted']);

const type = ref('IN');
const quantity = ref(1);
const isSubmitting = ref(false);
const errorMessage = ref('');

watch(() => props.isOpen, (newVal) => {
  if (newVal) {
    type.value = 'IN';
    quantity.value = 1;
    errorMessage.value = '';
  }
});

function closeModal() {
  errorMessage.value = '';
  emit('close');
}

async function handleSubmit() {
  if (!quantity.value || quantity.value <= 0) {
    errorMessage.value = 'La cantidad debe ser un número entero mayor a 0.';
    return;
  }

  const currentStock = Number(props.product?.stock || 0);

  if (type.value === 'OUT' && quantity.value > currentStock) {
    errorMessage.value = `Stock insuficiente. Intenta retirar ${quantity.value} u. pero solo hay ${currentStock} u. disponibles.`;
    return;
  }

  if (type.value === 'IN' && (currentStock + Number(quantity.value)) > 10000) {
    errorMessage.value = `No se puede superar el stock máximo permitido de 10.000 unidades. (Stock actual: ${currentStock} u.)`;
    return;
  }

  isSubmitting.value = true;
  errorMessage.value = '';

  const targetId = props.product._id || props.product.id;
  const delta = type.value === 'IN' ? Number(quantity.value) : -Number(quantity.value);
  const newStock = Math.min(10000, Math.max(0, currentStock + delta));

  try {
    const response = await axiosClient.patch(`/products/${targetId}/stock`, {
      type: type.value,
      quantity: Number(quantity.value)
    });

    const updatedProduct = {
      ...props.product,
      stock: response.data?.stock ?? newStock
    };
    emit('adjusted', updatedProduct);
  } catch (err) {
    const updatedProduct = {
      ...props.product,
      stock: newStock
    };
    emit('adjusted', updatedProduct);
  } finally {
    isSubmitting.value = false;
    closeModal();
  }
}
</script>
