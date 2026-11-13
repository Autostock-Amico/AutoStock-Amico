<template>
  <header class="navbar">
    <div class="navbar-inner">
      <router-link to="/dashboard" class="brand">
        <span class="brand-logo">A</span> AutoStock
      </router-link>

      <nav class="nav-links">
        <router-link to="/dashboard" class="nav-link">📦 Catálogo</router-link>
        <router-link to="/critical-stock" class="nav-link">⚠️ Stock crítico</router-link>
      </nav>

      <div class="nav-user">
        <span class="avatar">{{ username.charAt(0) }}</span>
        <span>{{ username }}</span>
        <button class="btn btn-secondary btn-sm" @click="handleLogout">Cerrar sesión</button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { logout, getCurrentUsername } from '../services/authService';

const router = useRouter();
const username = computed(() => getCurrentUsername());

const handleLogout = () => {
  logout();
  router.push('/login');
};
</script>