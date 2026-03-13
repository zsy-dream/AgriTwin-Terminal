<template>
  <div class="h-[calc(100vh-140px)] overflow-y-auto pr-2 custom-scrollbar">
    <div class="flex flex-col gap-4 pb-8 min-h-full">
      <div class="flex flex-col gap-4 xl:flex-row xl:items-center xl:justify-between py-2 px-4 border border-white/10 bg-white/5 rounded-xl">
        <h1 class="text-2xl font-semibold">高附加值作物多棚数字孪生监测总览</h1>
        <div class="flex items-center gap-3">
          <div class="text-sm text-slate-400">当前重点棚室</div>
          <div class="text-lg font-semibold text-cyber-neonCyan">{{ activeName }}</div>
        </div>
      </div>
      <!-- 顶部关键指标 -->
    <div class="grid grid-cols-5 gap-3 flex-shrink-0">
      <div class="rounded-xl border border-white/5 bg-white/3 p-3 flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg bg-cyber-neonViolet/20 flex items-center justify-center">
          <span class="text-lg">🏗️</span>
        </div>
        <div>
          <div class="text-xs text-slate-400">智能大棚</div>
          <div v-if="loading" class="h-6 w-16 bg-white/10 rounded animate-pulse mt-1" />
          <div v-else class="text-xl font-semibold">{{ summary.total_greenhouses }}<span class="text-xs text-slate-500 ml-1">座</span></div>
          <div class="text-[10px] text-slate-500 mt-1">联网接入与集中管控</div>
        </div>
      </div>
      
      <div class="rounded-xl border border-white/5 bg-white/3 p-3 flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg bg-cyber-neonPink/20 flex items-center justify-center">
          <span class="text-lg">⚠️</span>
        </div>
        <div>
          <div class="text-xs text-slate-400">活跃告警</div>
          <div v-if="loading" class="h-6 w-20 bg-white/10 rounded animate-pulse mt-1" />
          <div v-else class="text-xl font-semibold" :class="totalAlerts > 0 ? 'text-cyber-neonPink' : ''">{{ totalAlerts }}<span class="text-xs text-slate-500 ml-1">条</span></div>
          <div class="text-[10px] text-slate-500 mt-1">异常识别与分级提示</div>
        </div>
      </div>
      
      <div class="rounded-xl border border-white/5 bg-white/3 p-3 flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg bg-cyber-neonCyan/20 flex items-center justify-center">
          <span class="text-lg">📊</span>
        </div>
        <div>
          <div class="text-xs text-slate-400">曲线吻合度</div>
          <div v-if="loading" class="h-6 w-16 bg-white/10 rounded animate-pulse mt-1" />
          <div v-else class="text-xl font-semibold text-cyber-neonCyan">{{ activeAdherence }}%</div>
          <div class="text-[10px] text-slate-500 mt-1">目标带拟合程度</div>
        </div>
      </div>
      
      <div class="rounded-xl border border-white/5 bg-white/3 p-3 flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg bg-cyber-neonViolet/20 flex items-center justify-center">
          <span class="text-lg">🌱</span>
        </div>
        <div>
          <div class="text-xs text-slate-400">当前作物</div>
          <div v-if="loading" class="h-6 w-20 bg-white/10 rounded animate-pulse mt-1" />
          <div v-else class="text-sm font-semibold truncate">{{ activeGreenhouse?.crop || '-' }}</div>
          <div class="text-[10px] text-slate-500 mt-1">展示主案例作物</div>
        </div>
      </div>
      
      <!-- 新增：系统状态 -->
      <div class="rounded-xl border border-white/5 bg-white/3 p-3 flex items-center gap-3">
        <div class="h-10 w-10 rounded-lg flex items-center justify-center" :class="systemStatus.class">
          <span class="text-lg">{{ systemStatus.icon }}</span>
        </div>
        <div>
          <div class="text-xs text-slate-400">系统状态</div>
          <div class="text-sm font-semibold" :class="systemStatus.textClass">{{ systemStatus.text }}</div>
          <div class="text-[10px] text-slate-500 mt-1">系统在线与告警状态</div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="grid grid-cols-12 gap-3 flex-1 min-h-0">
      <!-- 左侧驾驶舱 8列 -->
      <div class="col-span-8 flex flex-col gap-3">
        <!-- 图表卡片 - 明确高度 -->
        <GlassCard title="24小时环境曲线" class="h-[380px] flex flex-col">
          <template #right>
            <div class="flex items-center gap-3">
              <span v-if="wsConnected" class="flex items-center gap-1 text-xs text-cyber-neonCyan">
                <span class="h-1.5 w-1.5 rounded-full bg-cyber-neonCyan animate-pulse" />
                实时
              </span>
              <span v-else class="text-xs text-slate-500">已断开</span>
              <span class="text-xs text-slate-400">{{ activeName }} · {{ activeGreenhouse?.growth_stage || '生长期' }}</span>
            </div>
          </template>
          <div class="relative h-[380px] w-full">
            <div ref="chartEl" class="w-full h-full" />
            <div v-if="loading" class="absolute inset-0 flex items-center justify-center">
              <div class="relative h-12 w-12">
                <div class="absolute inset-0 rounded-full border-2 border-cyber-neonViolet/70 border-t-transparent animate-spin" />
              </div>
            </div>
          </div>
        </GlassCard>
        
        <!-- 底部操作栏 - 固定高度 -->
        <div class="flex-shrink-0 flex items-center justify-between gap-3 p-2 rounded-xl border border-white/5 bg-white/3">
          <div class="flex items-center gap-3">
            <!-- 设备状态指示器 -->
            <div class="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-white/5">
              <span class="text-xs text-slate-400">设备:</span>
              <span 
                class="flex items-center gap-1 text-xs px-2 py-0.5 rounded"
                :class="equipmentStatus.irrigation ? 'bg-cyber-neonCyan/20 text-cyber-neonCyan' : 'bg-white/5 text-slate-500'"
              >
                <span class="h-1 w-1 rounded-full" :class="equipmentStatus.irrigation ? 'bg-cyber-neonCyan animate-pulse' : 'bg-slate-500'" />
                💧 {{ equipmentStatus.irrigation ? '灌溉中' : '空闲' }}
              </span>
              <span 
                class="flex items-center gap-1 text-xs px-2 py-0.5 rounded"
                :class="equipmentStatus.ventilation > 0 ? 'bg-cyber-neonViolet/20 text-cyber-neonViolet' : 'bg-white/5 text-slate-500'"
              >
                🌬️ {{ equipmentStatus.ventilation }}%
              </span>
            </div>
            
            <div class="w-px h-6 bg-white/10" />
            
            <template v-if="authStore.canControl">
              <NeonButton size="sm" :loading="actionLoading" @click="doIrrigate(60)">
                <span class="mr-1">💧</span> 灌溉 60s
              </NeonButton>
              <NeonButton size="sm" variant="ghost" :loading="actionLoading" @click="doIrrigate(180)">
                <span class="mr-1">💧</span> 灌溉 180s
              </NeonButton>
            </template>
            <template v-else>
              <span class="text-xs text-slate-500 px-2">🔒 观察员模式 - 无控制权限</span>
            </template>
          </div>
          
          <div class="flex items-center gap-4 text-xs">
            <div class="text-slate-400">
              大棚: <span class="text-cyber-neonCyan">{{ activeName }}</span>
            </div>
            <div class="text-slate-400">
              生长: <span class="text-cyber-neonViolet">{{ activeGreenhouse?.growth_stage || '-' }}</span>
              <span class="text-slate-500 ml-1">({{ activeGreenhouse?.growth_days || 0 }}/{{ activeGreenhouse?.expected_harvest_days || 0 }}天)</span>
            </div>
          </div>
        </div>

        <!-- 底部信息卡片：移入左侧以填补空白 -->
        <div class="grid grid-cols-2 gap-3 flex-shrink-0 h-[200px]">
          <!-- 告警列表 - 增强版 -->
          <GlassCard title="实时告警" class="h-full flex flex-col">
            <template #right>
              <button 
                v-if="alerts.filter(a => !a.acknowledged).length > 0 && authStore.canControl"
                @click="acknowledgeAllAlerts"
                class="text-xs text-cyber-neonCyan hover:text-cyber-neonViolet transition-colors"
              >
                全部确认
              </button>
            </template>
            <div class="flex-1 overflow-y-auto pr-1 space-y-1.5">
              <div v-if="alertsLoading" class="space-y-2">
                <div class="h-12 w-full bg-white/10 rounded animate-pulse" v-for="i in 3" :key="i" />
              </div>
              <template v-else-if="alerts.length">
                <div 
                  v-for="alert in alerts.slice(0, 5)" 
                  :key="alert.id"
                  class="p-2 rounded-lg border text-[11px] relative group"
                  :class="[
                    alert.level === 'critical' ? 'border-cyber-neonPink/20 bg-cyber-neonPink/5' : 
                    alert.level === 'warning' ? 'border-cyber-neonViolet/20 bg-cyber-neonViolet/5' : 
                    'border-cyber-neonCyan/20 bg-cyber-neonCyan/5',
                    alert.acknowledged ? 'opacity-50' : ''
                  ]"
                >
                  <div class="flex items-center gap-1 mb-0.5">
                    <div class="h-1.5 w-1.5 rounded-full" :class="alert.level === 'critical' ? 'bg-cyber-neonPink animate-pulse' : alert.level === 'warning' ? 'bg-cyber-neonViolet' : 'bg-cyber-neonCyan'" />
                    <span class="font-medium" :class="alert.level === 'critical' ? 'text-cyber-neonPink' : alert.level === 'warning' ? 'text-cyber-neonViolet' : 'text-cyber-neonCyan'">
                      {{ alert.level === 'critical' ? '紧急' : alert.level === 'warning' ? '预警' : '提示' }}
                    </span>
                    <span v-if="alert.acknowledged" class="ml-auto text-[9px] px-1 py-0.5 rounded bg-white/10 text-slate-400">已确认</span>
                    <button 
                      v-else-if="authStore.canControl"
                      @click="acknowledgeAlert(alert.id)"
                      class="ml-auto text-[9px] px-1.5 py-0.5 rounded bg-cyber-neonCyan/20 text-cyber-neonCyan hover:bg-cyber-neonCyan/30 transition-colors"
                    >
                      确认
                    </button>
                  </div>
                  <div class="text-slate-300 leading-tight">{{ alert.message }}</div>
                  <div class="text-[9px] text-slate-500 mt-1">{{ alert.greenhouse_name }} · {{ formatTime(alert.ts) }}</div>
                </div>
              </template>
              <div v-else class="text-center text-slate-400 py-4 text-xs">暂无活跃告警</div>
            </div>
          </GlassCard>

          <!-- SOP任务 -->
          <GlassCard title="SOP任务" class="h-full flex flex-col">
            <div class="flex-1 space-y-1 overflow-y-auto pr-1">
              <div v-if="tasksLoading" class="space-y-1">
                <div class="h-8 w-full bg-white/10 rounded animate-pulse" v-for="i in 3" :key="i" />
              </div>
              <template v-else-if="tasks.length">
                <div 
                  v-for="task in tasks.slice(0, 6)" 
                  :key="task.id"
                  class="flex items-center gap-2 p-1.5 rounded border text-[11px]"
                  :class="task.status === 'completed' ? 'bg-cyber-neonCyan/10 border-cyber-neonCyan/20' : task.status === 'in_progress' ? 'bg-cyber-neonViolet/10 border-cyber-neonViolet/20' : 'bg-white/5 border-white/10'"
                >
                  <div class="h-4 w-4 rounded flex items-center justify-center text-[10px] flex-shrink-0"
                    :class="task.status === 'completed' ? 'bg-cyber-neonCyan/20 text-cyber-neonCyan' : task.status === 'in_progress' ? 'bg-cyber-neonViolet/20 text-cyber-neonViolet' : 'bg-white/10 text-slate-400'"
                  >
                    {{ task.status === 'completed' ? '✓' : task.status === 'in_progress' ? '●' : '○' }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="truncate" :class="task.status === 'completed' ? 'text-slate-400' : 'text-slate-200'">{{ task.title }}</div>
                    <div class="text-[9px] text-slate-500">{{ task.scheduled_time }}</div>
                  </div>
                </div>
              </template>
              <div v-else class="text-center text-slate-400 py-2 text-xs">暂无任务</div>
            </div>
          </GlassCard>
        </div>
      </div>

      <!-- 右侧信息栏 4列 - 限制高度并允许滚动，防止覆盖 -->
      <div class="col-span-4 flex flex-col gap-3 h-[calc(100vh-140px)] overflow-y-auto pr-1">
        <!-- 3D虚拟大棚 -->
        <GlassCard title="Plant Factory 3D" class="flex-shrink-0 h-[220px]">
          <template #right>
            <span class="text-xs text-slate-400">{{ activeGreenhouse?.growth_stage || '生长期' }}</span>
          </template>
          <Greenhouse3D 
            :stageName="activeGreenhouse?.growth_stage || '生长期'" 
            :dayProgress="harvestProgress"
          />
        </GlassCard>

        <!-- 棚群选择 - 增强版 - 扩大高度并下移 -->
        <GlassCard title="棚群监控" class="flex-shrink-0 h-[280px]">
          <div class="grid grid-cols-1 gap-1.5 h-[240px] overflow-y-auto pr-1">
            <button 
              v-for="g in summary.top_risk" 
              :key="g.id"
              @click="setActive(g.id)"
              class="flex items-center justify-between p-2.5 rounded-lg border text-left transition-all shrink-0"
              :class="activeGreenhouseId === g.id ? 'border-cyber-neonViolet bg-cyber-neonViolet/10' : 'border-white/5 bg-white/3 hover:border-cyber-neonViolet/30'"
            >
              <div class="flex items-center gap-2">
                <div 
                  class="h-7 w-7 rounded flex items-center justify-center text-xs"
                  :class="g.active_alerts_count > 0 ? 'bg-cyber-neonPink/20' : 'bg-cyber-neonViolet/20'"
                >
                  {{ g.active_alerts_count > 0 ? '⚠️' : '🌱' }}
                </div>
                <div>
                  <div class="text-xs font-medium flex items-center gap-1">
                    {{ g.name }}
                    <span v-if="g.active_alerts_count > 0" class="px-1 py-0.5 rounded-full bg-cyber-neonPink/20 text-cyber-neonPink text-[9px]">
                      {{ g.active_alerts_count }}
                    </span>
                  </div>
                  <div class="text-[10px] text-slate-400">{{ g.crop }} · {{ g.growth_stage }}</div>
                </div>
              </div>
              <div class="text-right">
                <div 
                  class="text-xs font-medium"
                  :class="g.risk_score > 50 ? 'text-cyber-neonPink' : g.risk_score > 30 ? 'text-cyber-neonViolet' : 'text-cyber-neonCyan'"
                >
                  {{ g.risk_score }}
                </div>
                <div class="text-[9px] text-slate-400">{{ g.curve_adherence_pct }}%</div>
              </div>
            </button>
          </div>
        </GlassCard>

        <!-- 生长进度 - 增强版 -->
        <GlassCard title="作物生长进度" class="flex-shrink-0 h-[225px]">
          <div v-if="loading" class="space-y-2">
            <div class="h-4 w-full bg-white/10 rounded animate-pulse" />
            <div class="h-8 w-full bg-white/10 rounded animate-pulse" />
          </div>
          <div v-else-if="activeGreenhouse" class="space-y-4 py-2">
            <!-- 进度条 -->
            <div class="space-y-1">
              <div class="flex justify-between text-xs">
                <span class="text-slate-400">采收进度</span>
                <span class="text-cyber-neonCyan">{{ harvestProgressPercent }}%</span>
              </div>
              <div class="h-2 bg-white/10 rounded-full overflow-hidden">
                <div 
                  class="h-full bg-gradient-to-r from-cyber-neonViolet to-cyber-neonCyan rounded-full transition-all duration-500"
                  :style="{ width: harvestProgressPercent + '%' }"
                />
              </div>
            </div>

            <!-- 关键指标 -->
            <div class="grid grid-cols-3 gap-2 text-center">
              <div class="p-2 rounded bg-white/5">
                <div class="text-xs text-slate-400">已生长</div>
                <div class="text-sm font-semibold text-cyber-neonCyan">{{ activeGreenhouse?.growth_days || 0 }}天</div>
              </div>
              <div class="p-2 rounded bg-white/5">
                <div class="text-xs text-slate-400">预计剩余</div>
                <div class="text-sm font-semibold text-cyber-neonViolet">
                  {{ Math.max(0, (activeGreenhouse?.expected_harvest_days || 0) - (activeGreenhouse?.growth_days || 0)) }}天
                </div>
              </div>
              <div class="p-2 rounded bg-white/5">
                <div class="text-xs text-slate-400">总周期</div>
                <div class="text-sm font-semibold text-slate-200">{{ activeGreenhouse?.expected_harvest_days || '-' }}天</div>
              </div>
            </div>
          </div>
          <div v-else class="text-center text-slate-400 py-4 text-xs">暂无数据</div>
        </GlassCard>
      </div>
    </div>
  </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

import { acknowledgeDashboardAlert, getDashboardSummary, getTimeseries } from '../api/dashboard'
import { irrigate } from '../api/control'
import { getStages, getAlerts, getTasks } from '../api/operations'

import { useWebSocket } from '../composables/useWebSocket'
import { useAuthStore } from '../stores/auth.js'

import Greenhouse3D from '../components/Greenhouse3D.vue'
import GlassCard from '../components/GlassCard.vue'
import NeonButton from '../components/NeonButton.vue'

const authStore = useAuthStore()

const loading = ref(true)
const actionLoading = ref(false)

const summary = ref({
  total_greenhouses: 0,
  top_risk: [],
  latest_by_greenhouse: {}
})

const activeGreenhouseId = ref(1)

const stages = ref(null)
const stagesLoading = ref(false)
const alerts = ref([])
const alertsLoading = ref(false)
const tasks = ref([])
const tasksLoading = ref(false)

const chartEl = ref(null)
let chart = null
let timer = null
// Active mode not needed

// WS: 切换大棚自动重连
const { connected: wsConnected, realtimeData } = useWebSocket(activeGreenhouseId)

// 本地维护曲线数据，WS来一条就滚动更新
const wsPoints = ref([])

const activeName = computed(() => {
  const g = summary.value.top_risk.find((x) => x.id === activeGreenhouseId.value)
  return g ? g.name : `${activeGreenhouseId.value}号棚`
})

const activeGreenhouse = computed(() => {
  return summary.value.top_risk.find((x) => x.id === activeGreenhouseId.value)
})

const activeLatest = computed(() => {
  return summary.value.latest_by_greenhouse?.[activeGreenhouseId.value]
})

const activeAdherence = computed(() => {
  const g = summary.value.top_risk.find((x) => x.id === activeGreenhouseId.value)
  return g ? g.curve_adherence_pct : 0
})

// Removed presentation modes

// 新增：总告警数
const totalAlerts = computed(() => {
  return summary.value.top_risk?.reduce((sum, g) => sum + (g.active_alerts_count || 0), 0) || 0
})

// 新增：系统状态
const systemStatus = computed(() => {
  const criticalAlerts = alerts.value?.filter(a => a.level === 'critical' && !a.acknowledged).length || 0
  const warningAlerts = alerts.value?.filter(a => a.level === 'warning' && !a.acknowledged).length || 0
  
  if (criticalAlerts > 0) {
    return { text: '紧急告警', icon: '🔴', class: 'bg-cyber-neonPink/20', textClass: 'text-cyber-neonPink' }
  } else if (warningAlerts > 0) {
    return { text: '需要关注', icon: '🟡', class: 'bg-cyber-neonViolet/20', textClass: 'text-cyber-neonViolet' }
  } else if (wsConnected.value) {
    return { text: '运行正常', icon: '🟢', class: 'bg-cyber-neonCyan/20', textClass: 'text-cyber-neonCyan' }
  } else {
    return { text: '连接断开', icon: '⚪', class: 'bg-white/10', textClass: 'text-slate-400' }
  }
})

// 新增：采收进度
const harvestProgress = computed(() => {
  const g = activeGreenhouse.value
  if (!g || !g.expected_harvest_days) return 0.5
  return Math.min(1, g.growth_days / g.expected_harvest_days)
})

// 新增：采收进度百分比
const harvestProgressPercent = computed(() => {
  return Math.round(harvestProgress.value * 100)
})

// Removed regulationBenefits and heatmaps as per formal demo req

// 新增：设备状态（模拟）
const equipmentStatus = computed(() => {
  // 从温室详情获取，这里先模拟
  const gh = summary.value.latest_by_greenhouse?.[activeGreenhouseId.value]
  return {
    irrigation: gh?.soil_moisture_pct < 30,  // 土壤湿度低时显示灌溉中
    ventilation: Math.round((gh?.air_temp_c > 25 ? 60 : gh?.air_temp_c < 18 ? 20 : 40)),
    shading: gh?.light_lux > 45000,
    heating: gh?.air_temp_c < 15
  }
})

// 新增：格式化时间
function formatTime(ts) {
  if (!ts) return '-'
  const date = new Date(ts)
  const now = new Date()
  const diff = Math.floor((now - date) / 1000 / 60) // 分钟
  
  if (diff < 1) return '刚刚'
  if (diff < 60) return `${diff}分钟前`
  if (diff < 1440) return `${Math.floor(diff / 60)}小时前`
  return `${Math.floor(diff / 1440)}天前`
}

// 新增：确认告警
async function acknowledgeAlert(alertId) {
  try {
    await acknowledgeDashboardAlert(alertId)
    const alert = alerts.value.find(a => a.id === alertId)
    if (alert) alert.acknowledged = true
    toast('success', '告警已确认')
  } catch (e) {
    toast('error', '确认失败')
  }
}

// 新增：确认所有告警
async function acknowledgeAllAlerts() {
  try {
    const pendingAlerts = alerts.value.filter(a => !a.acknowledged)
    await Promise.all(pendingAlerts.map(a => acknowledgeDashboardAlert(a.id)))
    alerts.value.forEach(a => {
      a.acknowledged = true
    })
    toast('success', '全部告警已确认')
  } catch (e) {
    toast('error', '确认失败')
  }
}

function toast(type, msg) {
  window.dispatchEvent(new CustomEvent('app-toast', { detail: { type, msg } }))
}

async function setActive(id) {
  activeGreenhouseId.value = id
  stagesLoading.value = true
  alertsLoading.value = true
  tasksLoading.value = true
  try {
    const [st, al, ta] = await Promise.all([
      getStages(id),
      getAlerts(id),
      getTasks(id)
    ])
    stages.value = st
    alerts.value = al
    tasks.value = ta
    await refreshChart()
  } finally {
    stagesLoading.value = false
    alertsLoading.value = false
    tasksLoading.value = false
  }
}

async function load() {
  loading.value = true
  stagesLoading.value = true
  alertsLoading.value = true
  tasksLoading.value = true
  try {
    summary.value = await getDashboardSummary()
    if (summary.value.top_risk?.[0]?.id) activeGreenhouseId.value = summary.value.top_risk[0].id
    
    const [st, al, ta] = await Promise.all([
      getStages(activeGreenhouseId.value),
      getAlerts(activeGreenhouseId.value),
      getTasks(activeGreenhouseId.value)
    ])
    stages.value = st
    alerts.value = al
    tasks.value = ta
    
    await nextTick()
    await initChart()
  } finally {
    loading.value = false
    stagesLoading.value = false
    alertsLoading.value = false
    tasksLoading.value = false
  }
}

async function initChart() {
  if (!chartEl.value) return
  
  await nextTick()
  await new Promise(r => setTimeout(r, 300)) // 增加等待时间确保 DOM 就绪
  
  // 生成测试数据确保图表能显示
  const now = new Date()
  const testPoints = []
  for (let i = 23; i >= 0; i--) {
    const ts = new Date(now.getTime() - i * 60 * 1000 * 60)
    const hour = ts.getHours()
    testPoints.push({
      ts: ts.toISOString(),
      air_temp_c: 22 + 5 * Math.sin((hour - 6) * Math.PI / 12) + Math.random() * 2,
      air_humidity_pct: 65 - 10 * Math.sin((hour - 6) * Math.PI / 12) + Math.random() * 5,
      soil_moisture_pct: 35 + Math.random() * 3
    })
  }
  
  // 确保即使后端断开也有测试数据展示
  wsPoints.value = testPoints
  
  // 尝试获取真实数据进行覆盖
  try {
    const ts = await getTimeseries(activeGreenhouseId.value)
    if (ts && ts.points && ts.points.length > 1) {
      wsPoints.value = ts.points
    }
  } catch (e) {
    console.log('Using test data')
  }
  
  if (chart) {
    chart.dispose()
    chart = null
  }
  
  chart = echarts.init(chartEl.value)

  const x = wsPoints.value.map((p) => p.ts?.slice(11, 16) || '--')
  const temp = wsPoints.value.map((p) => p.air_temp_c)
  const hum = wsPoints.value.map((p) => p.air_humidity_pct)
  const soil = wsPoints.value.map((p) => p.soil_moisture_pct)

  const option = {
    backgroundColor: 'transparent',
    grid: { left: 50, right: 20, top: 40, bottom: 30 },
    tooltip: { 
      trigger: 'axis',
      backgroundColor: 'rgba(10, 10, 30, 0.9)',
      borderColor: 'rgba(139, 92, 246, 0.3)',
      textStyle: { color: '#e2e8f0', fontSize: 11 },
      formatter: (params) => {
        let res = `<div class="text-[11px] font-medium mb-1">${params[0].name}</div>`
        params.forEach(item => {
          res += `<div class="flex items-center gap-2 text-[10px]">
                    <span class="h-1.5 w-1.5 rounded-full" style="background:${item.color}"></span>
                    <span class="text-slate-400">${item.seriesName}:</span>
                    <span class="font-medium">${item.value}</span>
                  </div>`
        })
        return res
      }
    },
    legend: {
      data: ['温度', '湿度', '土壤水分'],
      textStyle: { color: '#94a3b8', fontSize: 11 },
      top: 10
    },
    xAxis: {
      type: 'category',
      data: x,
      axisLine: { lineStyle: { color: 'rgba(148,163,184,.35)' } },
      axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      splitLine: { lineStyle: { color: 'rgba(148,163,184,.12)' } },
      axisLabel: { 
        color: 'rgba(226,232,240,.7)', 
        fontSize: 10,
        formatter: (value) => value + (value > 100 ? '' : '')
      }
    },
    series: [
      {
        name: '温度',
        type: 'line',
        smooth: true,
        data: temp,
        showSymbol: false,
        lineStyle: { width: 2, color: '#8B5CF6' },
        areaStyle: { color: 'rgba(139,92,246,.15)' }
      },
      {
        name: '湿度',
        type: 'line',
        smooth: true,
        data: hum,
        showSymbol: false,
        lineStyle: { width: 2, color: '#EC4899' },
        areaStyle: { color: 'rgba(236,72,153,.12)' }
      },
      {
        name: '土壤水分',
        type: 'line',
        smooth: true,
        data: soil,
        showSymbol: false,
        lineStyle: { width: 2, color: '#22D3EE' },
        areaStyle: { color: 'rgba(34,211,238,.1)' }
      }
    ]
  }
  
  chart.setOption(option)
  
  setTimeout(() => {
    chart && chart.resize()
  }, 50)
}

function pushRealtimePoint({ timestamp, readings }) {
  if (!timestamp || !readings) return
  const ts = timestamp.endsWith('Z') ? timestamp : `${timestamp}Z`
  const p = {
    ts,
    air_temp_c: readings.air_temp_c,
    air_humidity_pct: readings.air_humidity_pct,
    soil_moisture_pct: readings.soil_moisture_pct
  }
  wsPoints.value = [...wsPoints.value, p].slice(-24)
}

function renderChartFromPoints() {
  if (!chart) return
  const x = wsPoints.value.map((p) => p.ts.slice(11, 16))
  chart.setOption({
    xAxis: { data: x },
    series: [
      { data: wsPoints.value.map((p) => p.air_temp_c) },
      { data: wsPoints.value.map((p) => p.air_humidity_pct) },
      { data: wsPoints.value.map((p) => p.soil_moisture_pct) }
    ]
  })
}

async function refreshChart() {
  if (!chart) return
  await initChart()
}

async function doIrrigate(durationSec) {
  actionLoading.value = true
  try {
    const res = await irrigate({
      greenhouse_id: activeGreenhouseId.value,
      mode: 'manual',
      duration_sec: durationSec,
      reason: `演示：检测到干旱趋势，执行灌溉 ${durationSec}s`
    })
    toast('info', `已下发灌溉：${res.duration_sec}s（动作ID ${res.action_id}）`)
  } finally {
    actionLoading.value = false
  }
}

onMounted(async () => {
  await load()
  // 低频轮询：只刷新概览与操作数据（实时曲线由WS推送驱动）
  timer = setInterval(load, 20000)
  
  // 延迟绑定resize事件确保图表已初始化
  setTimeout(() => {
    window.addEventListener('resize', () => {
      if (chart) {
        chart.resize()
      }
    })
  }, 500)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
  chart?.dispose()
})

watch(
  () => realtimeData.value,
  async (msg) => {
    if (!msg) return
    if (msg.greenhouse_id !== activeGreenhouseId.value) return

    // 更新顶部最新读数（用于后续扩展显示）
    summary.value.latest_by_greenhouse = {
      ...(summary.value.latest_by_greenhouse || {}),
      [activeGreenhouseId.value]: {
        ...(summary.value.latest_by_greenhouse?.[activeGreenhouseId.value] || {}),
        ...msg.readings
      }
    }

    pushRealtimePoint({ timestamp: msg.timestamp, readings: msg.readings })
    if (!chart) {
      await nextTick()
      await initChart()
    } else {
      renderChartFromPoints()
    }
  }
)
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.5); }
</style>
