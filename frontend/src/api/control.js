import http from './http'

export const irrigate = (payload) => http.post('/control/irrigate', payload).then((r) => r.data)
