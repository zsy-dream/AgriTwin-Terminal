import { ref, onMounted, onUnmounted, watch, unref } from 'vue'

const WS_BASE_URL = import.meta.env.VITE_WS_BASE_URL || 'ws://localhost:8000/api/v1/ws'

export function useWebSocket(greenhouseId = null) {
  const connected = ref(false)
  const lastMessage = ref(null)
  const realtimeData = ref(null)
  const url = ref('')

  let ws = null
  let reconnectTimer = null
  let heartbeatTimer = null
  let shouldReconnect = true

  const resolveGreenhouseId = () => {
    try {
      if (typeof greenhouseId === 'function') return greenhouseId()
      return unref(greenhouseId)
    } catch {
      return greenhouseId
    }
  }

  const connect = () => {
    if (import.meta.env.VITE_USE_MOCK === 'true') {
      console.log('[Mock Socket] Simulating WebSocket connection...')
      connected.value = true

      // 模拟定时发送数据
      heartbeatTimer = setInterval(() => {
        const ghId = resolveGreenhouseId()
        const simulatedData = {
          type: 'realtime_update',
          data: {
            temperature: (24 + Math.random() * 4).toFixed(1),
            humidity: (60 + Math.random() * 10).toFixed(0),
            light: (12000 + Math.random() * 2000).toFixed(0),
            co2: (400 + Math.random() * 100).toFixed(0),
            timestamp: new Date().toLocaleTimeString()
          }
        }
        lastMessage.value = simulatedData
        realtimeData.value = simulatedData.data
      }, 3000)

      return
    }

    const ghId = resolveGreenhouseId()
    const nextUrl = ghId ? `${WS_BASE_URL}/greenhouse/${ghId}` : `${WS_BASE_URL}/global`
    url.value = nextUrl

    ws = new WebSocket(nextUrl)

    ws.onopen = () => {
      connected.value = true
      startHeartbeat()
    }

    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data)
        lastMessage.value = data

        if (data.type === 'realtime_update') {
          realtimeData.value = data.data
        }
      } catch (e) {
        // ping/pong or plain text
        if (event.data === 'pong') {
          console.log('Heartbeat received')
        }
      }
    }

    ws.onclose = () => {
      connected.value = false
      stopHeartbeat()
      // 自动重连
      if (shouldReconnect) reconnectTimer = setTimeout(connect, 3000)
    }

    ws.onerror = (error) => {
      console.error('WebSocket error:', error)
    }
  }

  const startHeartbeat = () => {
    heartbeatTimer = setInterval(() => {
      if (ws?.readyState === WebSocket.OPEN) {
        ws.send('ping')
      }
    }, 25000) // 每25秒心跳
  }

  const stopHeartbeat = () => {
    if (heartbeatTimer) {
      clearInterval(heartbeatTimer)
      heartbeatTimer = null
    }
  }

  const disconnect = () => {
    shouldReconnect = false
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    stopHeartbeat()
    if (ws) {
      ws.close()
      ws = null
    }
  }

  const reconnect = () => {
    shouldReconnect = true
    if (reconnectTimer) {
      clearTimeout(reconnectTimer)
      reconnectTimer = null
    }
    stopHeartbeat()
    if (ws) {
      ws.close()
      ws = null
    }
    connect()
  }

  const send = (payload) => {
    if (!ws || ws.readyState !== WebSocket.OPEN) return false
    if (typeof payload === 'string') ws.send(payload)
    else ws.send(JSON.stringify(payload))
    return true
  }

  onMounted(() => {
    connect()
  })

  onUnmounted(() => {
    disconnect()
  })

  watch(
    () => resolveGreenhouseId(),
    (next, prev) => {
      if (next === prev) return
      // 切换大棚时重连
      shouldReconnect = true
      disconnect()
      shouldReconnect = true
      connect()
    }
  )

  return {
    connected,
    lastMessage,
    realtimeData,
    url,
    connect,
    reconnect,
    disconnect,
    send
  }
}
