import axios from 'axios'

import { handleMockRequest } from './mock'

const http = axios.create({
  baseURL: `${import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'}/api/v1`,
  timeout: 15000
})

// 使用自定义适配器实现 Mock
const defaultAdapter = axios.defaults.adapter
http.defaults.adapter = async (config) => {
  if (import.meta.env.VITE_USE_MOCK === 'true') {
    const mockRes = handleMockRequest(config)
    if (mockRes) {
      const [status, data] = mockRes
      return {
        data,
        status,
        statusText: 'OK',
        headers: config.headers,
        config,
        request: {}
      }
    }
  }
  return defaultAdapter(config)
}

http.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  },
  (error) => Promise.reject(error)
)

http.interceptors.response.use(
  (resp) => resp,
  (error) => {
    const msg = error?.response?.data?.detail || error.message || '请求失败'
    window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'error', msg } }))
    return Promise.reject(error)
  }
)

export default http
