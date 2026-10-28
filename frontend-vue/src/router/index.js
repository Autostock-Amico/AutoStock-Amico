import { createRouter, createWebHistory } from 'vue-router';
import { h } from 'vue';
import LoginView from '../views/LoginView.vue';

const DashboardView = {
  render: () => h('div', { style: 'padding: 2rem; font-family: sans-serif;' }, [
    h('h1', 'Dashboard Principal (Vue)'),
    h('p', 'Bienvenido al sistema de inventario AutoStock.')
  ])
};

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: DashboardView,
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/login',
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token');

  if (to.path === '/dashboard' && !token) {
    next('/login');
  } else if (to.path === '/login' && token) {
    next('/dashboard');
  } else {
    next();
  }
});

export default router;
