import http from './http'

export const login = (username, password) => {
  const formData = new URLSearchParams()
  formData.append('username', username)
  formData.append('password', password)
  
  return http.post('/auth/token', formData, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(r => r.data)
}

export const getCurrentUser = () => http.get('/auth/me').then(r => r.data)
export const logout = () => http.post('/auth/logout').then(r => r.data)
