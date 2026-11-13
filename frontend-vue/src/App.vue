<template>
  <AppNavbar v-if="route.meta.requiresAuth" />
  <router-view />
</template>

<script setup>
import { useRoute } from 'vue-router';
import AppNavbar from './components/AppNavbar.vue';

const route = useRoute();
</script>