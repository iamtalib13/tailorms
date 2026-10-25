import { createRouter, createWebHistory } from 'vue-router';
import POS from './pages/POS.vue';

const routes = [
  {
    path: '/',
    redirect: '/pos',
  },
  {
    path: '/pos',
    name: 'POS',
    component: POS,
  },
];

const router = createRouter({
  history: createWebHistory('/'),
  routes,
});

export default router;
