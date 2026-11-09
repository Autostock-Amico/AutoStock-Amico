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

        <div style="display: flex; gap: 1rem; margin-bottom: 1rem;">
          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Precio Costo ($) *</label>
            <input
              v-model.number="form.costPrice"
              type="number"
              min="0"
              step="0.01"
              required
              style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
            />
          </div>
          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Precio Venta ($) *</label>
            <input
              v-model.number="form.salePrice"
              type="number"
              min="0"
              step="0.01"
              required
              style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
            />
          </div>
        </div>

        <div style="display: flex; gap: 1rem; margin-bottom: 1.5rem;">
          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Stock Actual (Máx 10.000) *</label>
            <input
              v-model.number="form.currentStock"
              type="number"
              min="0"
              max="10000"
              required
              style="width: 100%; padding: 0.5rem; border: 1px solid #ced4da; border-radius: 4px; box-sizing: border-box;"
            />
          </div>
          <div style="flex: 1;">
            <label style="display: block; font-size: 0.9rem; font-weight: bold; margin-bottom: 0.3rem;">Stock Mínimo *</label>
            <input
              v-model.number="form.minStock"
              type="number"
              min="0"
              max="10000"
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
import { createProduct, updateProduct, getApiErrorMessage } from '../services/productService';

const props = defineProps({
  isOpen: Boolean,
  productToEdit: Object
});

const emit = defineEmits(['close', 'saved']);

const SKU_REGEX = /^[A-Z]{3}-\d{3,}$/;
const MAX_STOCK = 10000;
const EMPTY_FORM = { sku: '', name: '', category: '', costPrice: 0, salePrice: 0, currentStock: 0, minStock: 0 };

const isSubmitting = ref(false);
const errorMessage = ref('');
const form = ref({ ...EMPTY_FORM });

const isEditing = computed(() => !!props.productToEdit?.id);

const fillForm = (product) => {
  form.value = product ? { ...EMPTY_FORM, ...pickFields(product) } : { ...EMPTY_FORM };
  errorMessage.value = '';
};

const pickFields = (product) =>
  Object.fromEntries(Object.keys(EMPTY_FORM).map(key => [key, product[key] ?? EMPTY_FORM[key]]));

watch(() => props.productToEdit, fillForm, { immediate: true });

const validate = (data) => {
  if (!SKU_REGEX.test(data.sku)) return 'El SKU debe contener 3 letras, un guión y al menos 3 números (Ej: ART-001).';
  if (!data.name.trim() || !data.category.trim()) return 'Por favor complete todos los campos obligatorios.';
  if (data.currentStock > MAX_STOCK) return 'El stock no puede superar el límite máximo de 10.000 unidades.';
  return '';
};

const closeModal = () => {
  fillForm(null);
  emit('close');
};

const handleSubmit = async () => {
  const data = { ...form.value, sku: form.value.sku.trim().toUpperCase() };
  errorMessage.value = validate(data);
  if (errorMessage.value) return;

  isSubmitting.value = true;
  try {
    const saved = isEditing.value
      ? await updateProduct(props.productToEdit.id, data)
      : await createProduct(data);
    emit('saved', saved);
    closeModal();
  } catch (err) {
    errorMessage.value = getApiErrorMessage(err, 'No se pudo guardar el producto.');
  } finally {
    isSubmitting.value = false;
  }
};
</script>
