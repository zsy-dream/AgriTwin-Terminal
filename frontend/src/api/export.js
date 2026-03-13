import http from './http'

export const exportData = (greenhouseId, format = 'csv', dateRange = null) => {
  const params = new URLSearchParams()
  if (greenhouseId) params.append('greenhouse_id', greenhouseId)
  params.append('format', format)
  if (dateRange) {
    params.append('start_date', dateRange[0])
    params.append('end_date', dateRange[1])
  }
  
  return http.get(`/export/data?${params.toString()}`, {
    responseType: 'blob'
  }).then(response => {
    // 创建下载链接
    const blob = new Blob([response.data])
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `greenhouse_data_${new Date().toISOString().slice(0, 10)}.${format}`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    return true
  })
}

export const getExportHistory = () => {
  return http.get('/export/history').then(r => r.data)
}
