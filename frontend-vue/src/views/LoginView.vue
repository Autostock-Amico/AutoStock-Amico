<template>
  <div class="auth-page">
    <form class="auth-card" @submit.prevent="handleSubmit">
      <h2>AutoStock - Login</h2>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <div class="field">
        <label class="form-label">Usuario o email</label>
        <input
          type="text"
          v-model="credentials.identifier"
          required
          class="form-control"
        />
      </div>

      <div class="field">
        <label class="form-label">Contraseña</label>
        <input
          type="password"
          v-model="credentials.password"
          required
          class="form-control"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="btn btn-block btn-success"
      >
        {{ loading ? 'Cargando...' : 'Iniciar Sesión' }}
      </button>

      <p class="auth-footer">
        ¿No tenés cuenta?
        <router-link to="/register">Crear cuenta</router-link>
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
