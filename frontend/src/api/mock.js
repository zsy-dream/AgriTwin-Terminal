/**
 * Mock 数据中心
 * 为演示环境提供静态数据支持
 * 严格对齐后端 API 响应格式 (app/api/v1/endpoints/...)
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
    total_greenhouses: 3,
    active_alerts: 2,
    today_operations: 12,
    avg_temperature: 24.5,
    avg_humidity: 62.1,
    avg_light: 12500,
    top_risk: [
      { id: 1, name: '1号温室 - 玫瑰', crop: '玫瑰', risk_score: 12, curve_adherence_pct: 94, score: 94 },
      { id: 2, name: '2号温室 - 蓝莓', crop: '蓝莓', risk_score: 45, curve_adherence_pct: 78, score: 78 },
      { id: 3, name: '3号温室 - 育苗', crop: '育苗', risk_score: 28, curve_adherence_pct: 85, score: 85 }
    ],
    latest_by_greenhouse: {
      "1": { air_temp_c: 26.2, air_humidity_pct: 58, light_lux: 15400, soil_moisture_pct: 62, timestamp: '2024-03-14 10:00:00' },
      "2": { air_temp_c: 24.1, air_humidity_pct: 65, light_lux: 11200, soil_moisture_pct: 55, timestamp: '2024-03-14 10:00:00' },
      "3": { air_temp_c: 25.5, air_humidity_pct: 60, light_lux: 13000, soil_moisture_pct: 58, timestamp: '2024-03-14 10:00:00' }
    },
    recent_alerts: [
      { id: 101, greenhouse_name: '1号温室', type: '温度过高', level: 'warning', created_at: '2024-03-14 10:25:00', message: '当前温度 28°C，建议开启遮阳网' },
      { id: 102, greenhouse_name: '2号温室', type: '低湿度', level: 'critical', created_at: '2024-03-14 09:12:00', message: '土壤湿度低于 45%，触发自动灌溉' }
    ]
  },
  '/dashboard/timeseries': {
    greenhouse_id: 1,
    points: [
      { ts: '2024-03-14 00:00:00', air_temp_c: 18.2, air_humidity_pct: 75 },
      { ts: '2024-03-14 02:00:00', air_temp_c: 17.5, air_humidity_pct: 78 },
      { ts: '2024-03-14 04:00:00', air_temp_c: 17.1, air_humidity_pct: 80 },
      { ts: '2024-03-14 06:00:00', air_temp_c: 19.5, air_humidity_pct: 72 },
      { ts: '2024-03-14 08:00:00', air_temp_c: 22.4, air_humidity_pct: 65 },
      { ts: '2024-03-14 10:00:00', air_temp_c: 25.1, air_humidity_pct: 60 },
      { ts: '2024-03-14 12:00:00', air_temp_c: 27.8, air_humidity_pct: 55 },
      { ts: '2024-03-14 14:00:00', air_temp_c: 28.5, air_humidity_pct: 52 },
      { ts: '2024-03-14 16:00:00', air_temp_c: 27.2, air_humidity_pct: 58 },
      { ts: '2024-03-14 18:00:00', air_temp_c: 24.5, air_humidity_pct: 62 },
      { ts: '2024-03-14 20:00:00', air_temp_c: 21.2, air_humidity_pct: 68 },
      { ts: '2024-03-14 22:00:00', air_temp_c: 19.4, air_humidity_pct: 72 }
    ]
  },
  '/operations/stages/': {
    current_stage: { id: 2, name: '生长期', target_temp_min: 22, target_temp_max: 28, target_humidity_min: 55, target_humidity_max: 70 },
    days_in_stage: 15,
    all_stages: [
      { id: 1, name: '幼苗期', status: 'completed' },
      { id: 2, name: '生长期', status: 'active' },
      { id: 3, name: '开花期', status: 'upcoming' },
      { id: 4, name: '收获期', status: 'upcoming' }
    ]
  },
  '/operations/tasks': [
    { id: 1, title: '补充营养液', status: 'pending', scheduled_time: '今日 14:00' },
    { id: 2, title: '检查通风系统', status: 'pending', scheduled_time: '今日 16:30' },
    { id: 3, title: '日常巡检', status: 'completed', scheduled_time: '昨日' }
  ],
  '/operations/alerts': [
    { id: 1, title: '温度异常', message: '1号温室温度持续升高', level: 'warning', ts: '2024-03-14 10:25:00', auto_action: true }
  ],
  '/control/irrigate': {
    success: true,
    message: '指令已发送至控制器，正在执行灌溉...'
  }
}

export const handleMockRequest = (config) => {
  const url = config.url.replace(/^\/api\/v1/, '')
  console.log(`[Mock Server] Matching URL: ${url}`)

  // 查找匹配的路由
  const foundKey = Object.keys(mockData).find(key => url.startsWith(key))

  if (foundKey) {
    console.log(`[Mock Server] Intercepted: ${config.method.toUpperCase()} ${config.url}`)
    return [200, mockData[foundKey]]
  }

  return null
}
