import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

import { login as apiLogin, getCurrentUser, logout as apiLogout } from '../api/auth'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token') || null)
  const user = ref(null)
  const loading = ref(false)

  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const canControl = computed(() => ['admin', 'operator'].includes(user.value?.role))

  const setToken = (newToken) => {
    token.value = newToken
    if (newToken) {
      localStorage.setItem('token', newToken)
    } else {
      localStorage.removeItem('token')
    }
  }

  const login = async (username, password) => {
    loading.value = true
    try {
      const response = await apiLogin(username, password)
      setToken(response.access_token)
      await fetchUser()
      return { success: true }
    } catch (error) {
      return { 
        success: false, 
        message: error?.response?.data?.detail || '登录失败'
      }
    } finally {
      loading.value = false
    }
  }

  const fetchUser = async () => {
    try {
      user.value = await getCurrentUser()
      return true
    } catch (error) {
      setToken(null)
      return false
    }
  }

  const logout = async () => {
    try {
      await apiLogout()
    } finally {
      setToken(null)
      user.value = null
    }
  }

  const initAuth = async () => {
    if (token.value) {
      return await fetchUser()
    }
    return false
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    isAdmin,
    canControl,
    login,
    logout,
    fetchUser,
    initAuth,
    setToken
  }
})
