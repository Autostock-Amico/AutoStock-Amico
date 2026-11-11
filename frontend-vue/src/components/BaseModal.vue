<template>
  <div v-if="isOpen" class="modal-overlay">
    <div class="modal-card">
      <div class="modal-header">
        <h2>{{ title }}</h2>
        <button type="button" class="modal-close" @click="$emit('close')">&times;</button>
      </div>
      <slot />
    </div>
  </div>
</template>

<script setup>
defineProps({
  isOpen: Boolean,
  title: { type: String, required: true }
});

defineEmits(['close']);
</script>
