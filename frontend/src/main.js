import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import { useAuthStore } from './stores/auth'

import './styles/base.css'

(async () => {
  const pinia = createPinia()
  const authStore = useAuthStore(pinia)
  await authStore.initAuth()
  createApp(App).use(pinia).use(router).mount('#app')
})()
