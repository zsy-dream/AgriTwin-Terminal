import http from './http'

export const getStages = (greenhouseId) => http.get(`/operations/stages/${greenhouseId}`).then(r => r.data)
export const getAlerts = (greenhouseId) => http.get('/operations/alerts', { params: { greenhouse_id: greenhouseId } }).then(r => r.data)
export const getTasks = (greenhouseId) => http.get('/operations/tasks', { params: { greenhouse_id: greenhouseId } }).then(r => r.data)
export const completeTask = (taskId, notes) => http.post(`/operations/tasks/${taskId}/complete`, { notes }).then(r => r.data)
