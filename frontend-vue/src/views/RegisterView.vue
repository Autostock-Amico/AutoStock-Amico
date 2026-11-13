<template>
  <AuthLayout title="Crear cuenta" subtitle="Registrate para empezar a usar AutoStock">
    <form @submit.prevent="handleSubmit">
      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <IconInput v-model="form.username" label="Usuario" icon="👤" placeholder="Ej: santi" autocomplete="username" />
      <IconInput v-model="form.email" label="Email" icon="✉️" type="email" placeholder="tu@mail.com" autocomplete="email" />
      <IconInput
        v-model="form.password"
        label="Contraseña"
        icon="🔒"
        type="password"
        autocomplete="new-password"
        :hint="`Mínimo ${MIN_PASSWORD_LENGTH} caracteres`"
      />
      <IconInput v-model="form.confirmPassword" label="Repetir contraseña" icon="🔒" type="password" autocomplete="new-password" />

      <button type="submit" class="btn btn-primary btn-block auth-submit" :disabled="loading">
        {{ loading ? 'Creando cuenta...' : 'Crear cuenta' }}
      </button>

      <p class="auth-footer">
        ¿Ya tenés cuenta? <router-link to="/login">Iniciar sesión</router-link>
      </p>
    </form>
  </AuthLayout>
</template>

<script setup>
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import AuthLayout from '../components/AuthLayout.vue';
import IconInput from '../components/IconInput.vue';
import { register } from '../services/authService';
import { getApiErrorMessage } from '../services/productService';

const EMAIL_REGEX = /^\S+@\S+\.\S+$/;
const MIN_PASSWORD_LENGTH = 6;

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
      : 'No se pudo conectar con el servidor. Verificá que el backend esté encendido.';
  } finally {
    loading.value = false;
  }
};
</script>