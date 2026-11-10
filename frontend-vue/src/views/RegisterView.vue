<template>
  <div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-family: sans-serif; background-color: #f4f6f8;">
    <form @submit.prevent="handleSubmit" style="background: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); width: 340px;">
      <h2 style="text-align: center; margin-bottom: 1.5rem; color: #333;">AutoStock - Crear cuenta</h2>

      <div v-if="error" style="color: #721c24; background-color: #f8d7da; padding: 0.5rem; border-radius: 4px; margin-bottom: 1rem; font-size: 0.9rem;">
        {{ error }}
      </div>

      <div v-for="field in fields" :key="field.key" style="margin-bottom: 1rem;">
        <label style="display: block; margin-bottom: 0.5rem; font-size: 0.9rem;">{{ field.label }}</label>
        <input
          :type="field.type"
          v-model="form[field.key]"
          required
          style="width: 100%; padding: 0.5rem; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px;"
        />
      </div>

      <button
        type="submit"
        :disabled="loading"
        style="width: 100%; padding: 0.6rem; margin-top: 0.5rem; background-color: #0d6efd; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;"
      >
        {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
      </button>

      <p style="text-align: center; margin: 1rem 0 0; font-size: 0.9rem; color: #555;">
        ¿Ya tenés cuenta?
        <router-link to="/login" style="color: #0d6efd; font-weight: bold;">Iniciar sesión</router-link>
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
