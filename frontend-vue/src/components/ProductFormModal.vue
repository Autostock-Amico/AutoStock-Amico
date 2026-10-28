<template>
  <div v-if="isOpen" style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1000;">
    <div style="background: white; border-radius: 8px; width: 90%; max-width: 500px; padding: 2rem; box-shadow: 0 4px 10px rgba(0,0,0,0.15);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; color: #333;">{{ isEditing ? 'Editar Producto' : 'Nuevo Producto' }}</h2>
        <button @click="closeModal" style="background: transparent; border: none; font-size: 1.5rem; cursor: pointer; color: #6c757d;">&times;</button>
      </div>

      <div v-if="errorMessage" style="background: #f8d7da; color: #721c24; padding: 0.75rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="handleSubmit">
        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">SKU * (Ej: ART-001)</label>
          <input
            v-model="form.sku"
            type="text"
            required
            pattern="^[A-Za-z]{3}-\d{3,}$"
            title="El SKU debe tener 3 letras, un guión y 3 o más números (Ej: ART-001)"
            placeholder="Ej: ART-001"
            @input="form.sku = form.sku.toUpperCase()"
            style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
          />
        </div>

        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Nombre *</label>
          <input
            v-model="form.name"
            type="text"
            required
            placeholder="Ej: Filtro de Aceite"
            style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
          />
        </div>

        <div style="margin-bottom: 1rem;">
          <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Categoría *</label>
          <input
            v-model="form.category"
            type="text"
            required
            placeholder="Ej: Filtros, Lubricantes, Frenos"
            style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
          />
        </div>

        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Precio Venta ($) *</label>
            <input
              v-model.number="form.price"
              type="number"
              min="0"
              step="0.01"
              required
              style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
            />
          </div>

          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Stock Actual *</label>
            <input
              v-model.number="form.stock"
              type="number"
              min="0"
              required
              style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
            />
          </div>
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
            {{ isSubmitting ? 'Guardando...' : (isEditing ? 'Actualizar' : 'Crear Producto') }}
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';
import axiosClient from '../api/axiosClient';

const props = defineProps({
  isOpen: Boolean,
  productToEdit: Object
});

const emit = defineEmits(['close', 'saved']);

const isSubmitting = ref(false);
const errorMessage = ref('');

const isEditing = computed(() => !!props.productToEdit?._id || !!props.productToEdit?.id);

const form = ref({
  sku: '',
  name: '',
  category: '',
  price: 0,
  stock: 0
});

watch(() => props.productToEdit, (newVal) => {
  if (newVal) {
    form.value = {
      sku: newVal.sku || '',
      name: newVal.name || newVal.nombre || '',
      category: newVal.category || newVal.categoria || '',
      price: newVal.price || newVal.precio || 0,
      stock: newVal.stock || 0
    };
  } else {
    resetForm();
  }
}, { immediate: true, deep: true });

function resetForm() {
  form.value = { sku: '', name: '', category: '', price: 0, stock: 0 };
  errorMessage.value = '';
}

function closeModal() {
  resetForm();
  emit('close');
}

async function handleSubmit() {
  const formattedSku = form.value.sku.trim().toUpperCase();
  const skuRegex = /^[A-Z]{3}-\d{3,}$/;

  if (!skuRegex.test(formattedSku)) {
    errorMessage.value = 'El SKU debe contener 3 letras, un guión y al menos 3 números (Ej: ART-001).';
    return;
  }

  if (!form.value.name || !form.value.category) {
    errorMessage.value = 'Por favor complete todos los campos obligatorios.';
    return;
  }

  isSubmitting.value = true;
  errorMessage.value = '';

  const targetId = isEditing.value ? (props.productToEdit._id || props.productToEdit.id) : Date.now().toString();

  const formattedProduct = {
    id: targetId,
    _id: targetId,
    sku: formattedSku,
    name: form.value.name,
    category: form.value.category,
    price: Number(form.value.price),
    stock: Number(form.value.stock)
  };

  emit('saved', formattedProduct);

  try {
    if (isEditing.value) {
      await axiosClient.put(`/products/${targetId}`, formattedProduct);
    } else {
      await axiosClient.post('/products', formattedProduct);
    }
  } catch (err) {
    // Modo offline/demo local
  } finally {
    isSubmitting.value = false;
    closeModal();
  }
}
</script>
