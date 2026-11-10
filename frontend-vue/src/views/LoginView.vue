<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; background-color: #f4f6f8;">
    <form @submit.prevent="handleSubmit" style="background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 320px;">
      <h2 style="text-align: center; margin-bottom: 1.5rem; color: #333;">AutoStock - Login</h2>

      <div v-if="successMessage" style="color: #0f5132; background-color: #d1e7dd; padding: 0.5rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ successMessage }}
      </div>

      <div v-if="error" style="color: #721c24; background-color: #f8d7da; padding: 0.5rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ error }}
      </div>

      <div style="margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.9rem;">Usuario o email</label>
        <input
          type="text"
          v-model="credentials.identifier"
          required
          style="width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;"
        />
      </div>

      <div style="margin-bottom: 1.5rem;">
        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.9rem;">Contraseña</label>
        <input
          type="password"
          v-model="credentials.password"
          required
          style="width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        style="width: 100%; padding: 0.6rem; background-color: #42b983; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"
      >
        {{ loading ? 'Cargando...' : 'Iniciar Sesión' }}
      </button>

      <p style="text-align: center; margin: 1rem 0 0; font-size: 0.9rem; color: #555;">
        ¿No tenés cuenta?
        <router-link to="/register" style="color: #0d6efd; font-weight: bold;">Crear cuenta</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { login } from '../services/authService';
import { getApiErrorMessage } from '../services/productService';

const router = useRouter();
const route = useRoute();

const credentials = reactive({ identifier: '', password: '' });
const loading = ref(false);
const error = ref('');
const successMessage = ref(route.query.registered ? 'Cuenta creada. Ya podés iniciar sesión.' : '');

const handleSubmit = async () => {
  error.value = '';
  successMessage.value = '';
  loading.value = true;
  try {
    await login(credentials.identifier.trim(), credentials.password);
    router.push('/dashboard');
  } catch (err) {
    error.value = err.response
      ? getApiErrorMessage(err, 'Credenciales inválidas.')
      : 'Error al conectar con el servidor. Inténtalo nuevamente.';
  } finally {
    loading.value = false;
  }
};
</script>
