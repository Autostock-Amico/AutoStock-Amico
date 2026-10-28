<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; background-color: #f4f6f8;">
    <form @submit.prevent="handleSubmit" style="background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 320px;">
      <h2 style="text-align: center; margin-bottom: 1.5rem; color: #333;">AutoStock - Login</h2>

      <div v-if="error" style="color: #721c24; background-color: #f8d7da; padding: 0.5rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ error }}
      </div>

      <div style="margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.9rem;">Usuario</label>
        <input
          type="text"
          v-model="credentials.username"
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
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import axiosClient from '../api/axiosClient';

const router = useRouter();

const credentials = reactive({ username: '', password: '' });
const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
  error.value = '';
  loading.value = true;

  try {
    const response = await axiosClient.post('/auth/login', credentials);
    const { token } = response.data;

    if (token) {
      localStorage.setItem('token', token);
    }
    router.push('/dashboard');
  } catch (err) {
    if (err.response && err.response.status === 401) {
      error.value = 'Credenciales inválidas. Por favor, verifica tu usuario y contraseña.';
    } else {
      error.value = 'Error al conectar con el servidor. Inténtalo nuevamente.';
    }
  } finally {
    loading.value = false;
  }
};
</script>
