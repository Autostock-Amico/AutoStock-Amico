<template>
  <div class="toast-container">
    <div v-for="toast in toasts" :key="toast.id" class="toast" :class="{ 'is-error': toast.type === 'error' }">
      <span>{{ toast.type === 'error' ? '⚠️' : '✅' }}</span>
      <span>{{ toast.message }}</span>
      <button class="toast-close" @click="remove(toast.id)">×</button>
    </div>
  </div>
</template>

<script setup>
import { useToast } from '../composables/useToast';

const { toasts, remove } = useToast();
</script>