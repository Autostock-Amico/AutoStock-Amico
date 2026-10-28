import { createApp } from 'vue';
import { createPinia } from 'pinia';
import router from './router';
import { useAuthStore } from './stores/authStore';

const app = createApp({
  template: '<router-view></router-view>'
});

const pinia = createPinia();
app.use(pinia);

// Inicializar router después de Pinia
app.use(router);

app.mount('#app');
