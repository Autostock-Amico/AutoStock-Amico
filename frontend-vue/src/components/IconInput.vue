<template>
  <div class="field">
    <label class="form-label">{{ label }}</label>
    <div class="input-icon">
      <span class="icon">{{ icon }}</span>
      <input
        class="form-control"
        :class="{ 'has-toggle': isPassword }"
        :type="inputType"
        :value="modelValue"
        :placeholder="placeholder"
        :autocomplete="autocomplete"
        required
        @input="$emit('update:modelValue', $event.target.value)"
      />
      <button v-if="isPassword" type="button" class="toggle-password" @click="visible = !visible">
        {{ visible ? 'Ocultar' : 'Mostrar' }}
      </button>
    </div>
    <div v-if="hint" class="form-hint">{{ hint }}</div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  modelValue: { type: String, default: '' },
  label: { type: String, required: true },
  icon: { type: String, default: '' },
  type: { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  autocomplete: { type: String, default: 'off' },
  hint: { type: String, default: '' }
});

defineEmits(['update:modelValue']);

const visible = ref(false);
const isPassword = computed(() => props.type === 'password');
const inputType = computed(() => (isPassword.value && visible.value ? 'text' : props.type));
</script>