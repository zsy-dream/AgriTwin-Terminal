import http from './http'

export const getDashboardSummary = () => http.get('/dashboard/summary').then((r) => r.data)
export const getTimeseries = (greenhouseId) =>
  http.get('/dashboard/timeseries', { params: { greenhouse_id: greenhouseId } }).then((r) => r.data)
export const acknowledgeDashboardAlert = (alertId) =>
  http.post(`/dashboard/alerts/${alertId}/acknowledge`).then((r) => r.data)
