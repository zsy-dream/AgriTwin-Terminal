/**
 * Mock 数据中心
 * 为演示环境提供静态数据支持
 */

const mockData = {
  '/auth/token': {
    access_token: 'mock_token_123456',
    token_type: 'bearer'
  },
  '/auth/me': {
    id: 1,
    username: 'admin',
    full_name: '超级管理员',
    role: 'admin'
  },
  '/dashboard/summary': {
    total_greenhouses: 4,
    active_alerts: 2,
    today_operations: 12,
    avg_temperature: 24.5,
    avg_humidity: 62,
    avg_light: 12500,
    greenhouses: [
      { id: 1, name: '1号温室 - 玫瑰', status: 'online', temp: 26.2, humi: 58, light: 15400 },
      { id: 2, name: '2号温室 - 蓝莓', status: 'online', temp: 24.1, humi: 65, light: 11200 },
      { id: 3, name: '3号温室 - 育苗', status: 'online', temp: 25.5, humi: 60, light: 13000 },
      { id: 4, name: '4号温室 - 测试', status: 'offline', temp: 0, humi: 0, light: 0 }
    ],
    alerts: [
      { id: 101, greenhouse: '1号温室', type: '温度过高', level: 'warning', time: '10:25', content: '当前温度 28°C，建议开启遮阳网' },
      { id: 102, greenhouse: '2号温室', type: '低湿度', level: 'error', time: '09:12', content: '土壤湿度低于 45%，触发自动灌溉' }
    ]
  },
  '/dashboard/timeseries': {
    labels: ['00:00', '02:00', '04:00', '06:00', '08:00', '10:00', '12:00', '14:00', '16:00', '18:00', '20:00', '22:00'],
    datasets: [
      { label: '温度 (°C)', data: [18.2, 17.5, 17.1, 19.5, 22.4, 25.1, 27.8, 28.5, 27.2, 24.5, 21.2, 19.4] },
      { label: '湿度 (%)', data: [75, 78, 80, 72, 65, 60, 55, 52, 58, 62, 68, 72] }
    ]
  },
  '/operations/stages/1': [
    { title: '幼苗期', status: 'finish', date: '2024-03-01' },
    { title: '生长期', status: 'process', date: '2024-03-15' },
    { title: '开花期', status: 'wait', date: '-' },
    { title: '收获期', status: 'wait', date: '-' }
  ],
  '/operations/tasks': [
    { id: 1, title: '补充营养液', type: 'maintenance', time: '今日 14:00', status: 'pending' },
    { id: 2, title: '检查通风系统', type: 'inspection', time: '今日 16:30', status: 'pending' },
    { id: 3, title: '日常巡检', type: 'routine', time: '昨日', status: 'completed' }
  ],
  '/operations/alerts': [
    { id: 1, greenhouse_id: 1, type: '温度异常', content: '1号温室温度持续升高', level: 'warning', created_at: '2024-03-13 10:25:00' }
  ],
  '/control/irrigate': {
    success: true,
    message: '指令已发送至控制器，正在执行灌溉...'
  }
}

export const handleMockRequest = (config) => {
  const url = config.url.replace(/^\/api\/v1/, '')
  const foundKey = Object.keys(mockData).find(key => url.includes(key))
  
  if (foundKey) {
    console.log(`[Mock Server] Intercepted: ${config.method.toUpperCase()} ${config.url}`)
    return [200, mockData[foundKey]]
  }
  
  return null
}
