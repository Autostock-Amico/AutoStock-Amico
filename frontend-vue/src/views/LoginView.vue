<template>
  <AuthLayout title="Bienvenido a AutoStock" subtitle="Ingresá para gestionar tu inventario">
    <form @submit.prevent="handleSubmit">
      <div v-if="successMessage" class="alert alert-success">{{ successMessage }}</div>
      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <IconInput v-model="credentials.identifier" label="Usuario o email" icon="👤" placeholder="santi o santi@mail.com" autocomplete="username" />
      <IconInput v-model="credentials.password" label="Contraseña" icon="🔒" type="password" placeholder="Tu contraseña" autocomplete="current-password" />

      <button type="submit" class="btn btn-primary btn-block auth-submit" :disabled="loading">
        {{ loading ? 'Ingresando...' : 'Iniciar sesión' }}
      </button>

      <p class="auth-footer">
        ¿No tenés cuenta? <router-link to="/register">Crear cuenta</router-link>
      </p>
    </form>
  </AuthLayout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import AuthLayout from '../components/AuthLayout.vue';
import IconInput from '../components/IconInput.vue';
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
      : 'No se pudo conectar con el servidor. Verificá que el backend esté encendido.';
  } finally {
    loading.value = false;
  }
};
</script>