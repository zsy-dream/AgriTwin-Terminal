import { createRouter, createWebHistory } from 'vue-router'

import Dashboard from '../views/Dashboard.vue'
import Greenhouses from '../views/Greenhouses.vue'
import Login from '../views/Login.vue'
import Business from '../views/Business.vue'
import Pitch from '../views/Pitch.vue'
import Settings from '../views/Settings.vue'
import Showcase from '../views/Showcase.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', component: Login, meta: { public: true } },
  { path: '/pitch', component: Pitch, meta: { requiresAuth: true } },
  { path: '/showcase', component: Showcase, meta: { requiresAuth: true } },
  { path: '/business', component: Business, meta: { requiresAuth: true } },
  { path: '/dashboard', component: Dashboard, meta: { requiresAuth: true } },
  { path: '/greenhouses', component: Greenhouses, meta: { requiresAuth: true } },
  { path: '/settings', component: Settings, meta: { requiresAuth: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
