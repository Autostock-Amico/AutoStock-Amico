<template>
  <div class="auth-page">
    <form class="auth-card" @submit.prevent="handleSubmit">
      <h2>AutoStock - Crear cuenta</h2>

      <div v-if="error" class="alert alert-error">
        {{ error }}
      </div>

      <div v-for="field in fields" :key="field.key" class="field">
        <label class="form-label">{{ field.label }}</label>
        <input
          :type="field.type"
          v-model="form[field.key]"
          required
          class="form-control"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        class="btn btn-block btn-primary"
      >
        {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
      </button>

      <p class="auth-footer">
        ¿Ya tenés cuenta?
        <router-link to="/login">Iniciar sesión</router-link>
      </p>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { register } from '../services/authService';
import { getApiErrorMessage } from '../services/productService';

const EMAIL_REGEX = /^\S+@\S+\.\S+$/;
const MIN_PASSWORD_LENGTH = 6;

const fields = [
  { key: 'username', label: 'Usuario', type: 'text' },
  { key: 'email', label: 'Email', type: 'email' },
  { key: 'password', label: 'Contraseña', type: 'password' },
  { key: 'confirmPassword', label: 'Repetir contraseña', type: 'password' }
];

const router = useRouter();
const form = reactive({ username: '', email: '', password: '', confirmPassword: '' });
const loading = ref(false);
const error = ref('');

const validate = () => {
  if (!form.username.trim()) return 'El usuario es obligatorio.';
  if (!EMAIL_REGEX.test(form.email)) return 'El formato del email no es válido.';
  if (form.password.length < MIN_PASSWORD_LENGTH) return `La contraseña debe tener al menos ${MIN_PASSWORD_LENGTH} caracteres.`;
  if (form.password !== form.confirmPassword) return 'Las contraseñas no coinciden.';
  return '';
};

const handleSubmit = async () => {
  error.value = validate();
  if (error.value) return;

  loading.value = true;
  try {
    await register({ username: form.username.trim(), email: form.email.trim(), password: form.password });
    router.push({ path: '/login', query: { registered: '1' } });
  } catch (err) {
    error.value = err.response
      ? getApiErrorMessage(err, 'No se pudo crear la cuenta.')
      : 'Error al conectar con el servidor. Inténtalo nuevamente.';
  } finally {
    loading.value = false;
  }
};
</script>
