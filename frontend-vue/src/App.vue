<template>
  <AppNavbar v-if="route.meta.requiresAuth" />
  <router-view />
  <ToastContainer />
</template>

<script setup>
import { useRoute } from 'vue-router';
import AppNavbar from './components/AppNavbar.vue';
import ToastContainer from './components/ToastContainer.vue';

const route = useRoute();
</script>