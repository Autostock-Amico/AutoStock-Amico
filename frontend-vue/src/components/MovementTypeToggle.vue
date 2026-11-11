<template>
  <div class="row">
    <button
      v-for="option in OPTIONS"
      :key="option.value"
      type="button"
      class="btn"
      :style="buttonStyle(option)"
      @click="$emit('update:modelValue', option.value)"
    >
      {{ option.label }}
    </button>
  </div>
</template>

<script setup>
const props = defineProps({
  modelValue: { type: String, required: true }
});

defineEmits(['update:modelValue']);

const OPTIONS = [
  { value: 'IN', label: '+ Entrada (Ingreso)', color: '#198754' },
  { value: 'OUT', label: '- Salida (Egreso)', color: '#dc3545' }
];

const buttonStyle = (option) => {
  const active = props.modelValue === option.value;
  return {
    border: `1px solid ${option.color}`,
    backgroundColor: active ? option.color : '#fff',
    color: active ? '#fff' : option.color
  };
};
</script>
