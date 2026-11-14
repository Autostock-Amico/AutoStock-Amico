import { ref } from 'vue';

// Lista compartida de notificaciones (una sola para toda la app)
const toasts = ref([]);
let nextId = 1;

const DURATION_MS = 3500;

const remove = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id);
};

const show = (message, type) => {
  const id = nextId++;
  toasts.value = [...toasts.value, { id, message, type }];
  setTimeout(() => remove(id), DURATION_MS);
};

export function useToast() {
  return {
    toasts,
    remove,
    success: (message) => show(message, 'success'),
    error: (message) => show(message, 'error')
  };
}