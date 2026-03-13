<template>
  <div class="h-[calc(100vh-140px)] overflow-y-auto pr-2 custom-scrollbar">
    <div class="grid grid-cols-12 gap-6 pb-8">
      <!-- 左侧栏 -->
      <div class="col-span-4 flex flex-col gap-4">
        <GlassCard class="hud flex-shrink-0">
          <div class="space-y-3">
            <div class="inline-flex items-center gap-2 rounded-full border border-cyber-neonViolet/20 bg-cyber-neonViolet/10 px-3 py-1 text-xs text-cyber-neonViolet">
              多棚协同展示页
            </div>
            <div>
              <div class="text-lg font-semibold">高附加值作物棚群管理与对比</div>
              <div class="mt-1 text-xs leading-6 text-slate-400">
                面向评委展示多棚并行监测、阶段差异、风险分级和标准作业执行能力。
              </div>
            </div>
          </div>
        </GlassCard>
        <GlassCard title="棚群管理" class="hud flex-1 min-h-0">
          <div class="space-y-3 h-full overflow-auto pr-1">
            <div
              v-for="g in greenhouses"
              :key="g.id"
              @click="selectGreenhouse(g.id)"
              class="p-3 rounded-xl2 border cursor-pointer transition-all"
              :class="selectedId === g.id ? 'border-cyber-neonViolet bg-cyber-neonViolet/10' : 'border-white/5 bg-white/3 hover:border-cyber-neonViolet/30'"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center gap-2">
                  <div class="h-8 w-8 rounded-lg bg-cyber-neonViolet/20 flex items-center justify-center">
                    <span class="text-sm">🌱</span>
                  </div>
                  <div>
                    <div class="font-semibold text-sm">{{ g.name }}</div>
                    <div class="text-[10px] text-slate-400">{{ g.crop }} · 重点案例棚</div>
                  </div>
                </div>
                <div class="text-right">
                  <div class="text-xs" :class="g.risk_score > 50 ? 'text-cyber-neonPink' : 'text-cyber-neonCyan'">风险 {{ g.risk_score }}</div>
                  <div class="text-[10px] text-slate-400">达标 {{ g.curve_adherence_pct }}%</div>
                </div>
              </div>
              <div class="grid grid-cols-3 gap-2 text-[10px]">
                <div class="p-1.5 rounded bg-white/5 text-center">
                  <div class="text-slate-400">温度</div>
                  <div class="text-cyber-neonCyan">{{ g.latest?.air_temp_c }}℃</div>
                </div>
                <div class="p-1.5 rounded bg-white/5 text-center">
                  <div class="text-slate-400">湿度</div>
                  <div class="text-cyber-neonPink">{{ g.latest?.air_humidity_pct }}%</div>
                </div>
                <div class="p-1.5 rounded bg-white/5 text-center">
                  <div class="text-slate-400">土壤</div>
                  <div class="text-cyber-neonViolet">{{ g.latest?.soil_moisture_pct }}%</div>
                </div>
              </div>
            </div>
          </div>
        </GlassCard>
        <GlassCard title="批量操作" class="hud flex-shrink-0">
          <div class="grid grid-cols-2 gap-2">
            <NeonButton size="sm" @click="batchIrrigate">批量灌溉</NeonButton>
            <NeonButton size="sm" variant="ghost" @click="exportData">导出数据</NeonButton>
          </div>
        </GlassCard>
      </div>

      <!-- 右侧栏 -->
      <div class="col-span-8 flex flex-col gap-4">
        <GlassCard title="棚群横向对比" class="hud flex-shrink-0">
          <template #right>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="mode in compareModes"
                :key="mode.key"
                @click="activeCompareMode = mode.key"
                class="rounded-full px-3 py-1 text-[10px] transition-colors"
                :class="activeCompareMode === mode.key ? 'bg-cyber-neonViolet/20 text-cyber-neonViolet' : 'bg-white/5 text-slate-400'"
              >
                {{ mode.label }}
              </button>
            </div>
          </template>
          <div class="grid gap-4 xl:grid-cols-[1.15fr_0.85fr]">
            <div ref="compareChartEl" class="h-[220px]" />
            <div class="space-y-3">
              <div v-for="item in compareSummary" :key="item.label" class="rounded-xl border border-white/10 bg-white/5 p-3">
                <div class="mb-1 flex items-center justify-between text-xs">
                  <span class="text-slate-400">{{ item.label }}</span>
                  <span :class="item.color">{{ item.value }}</span>
                </div>
                <div class="text-[10px] leading-5 text-slate-500">{{ item.note }}</div>
              </div>
            </div>
          </div>
        </GlassCard>

        <template v-if="selectedGreenhouse">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4 rounded-xl border border-white/10 bg-white/5 p-4 mb-2">
          <div class="flex items-center gap-3">
            <div class="h-10 w-10 rounded-full bg-cyber-neonCyan/10 flex items-center justify-center text-lg">🏠</div>
            <div>
              <div class="text-lg font-semibold">{{ selectedGreenhouse.name }}</div>
              <div class="text-[11px] text-slate-500">数字孪生调控 · 重点数据下钻</div>
            </div>
            <span class="px-2 py-0.5 rounded-full bg-cyber-neonCyan/20 text-[10px] text-cyber-neonCyan">
              {{ selectedGreenhouse.crop }}
            </span>
          </div>
          <div class="flex items-center gap-3">
            <NeonButton size="sm" @click="refreshData">刷新数据</NeonButton>
            <NeonButton size="sm" variant="ghost" @click="goSettings">查看详情</NeonButton>
          </div>
        </div>

          <div class="grid grid-cols-2 gap-4">
            <GlassCard title="阶段管理" class="hud">
              <div v-if="stagesLoading" class="space-y-2">
                <SkeletonBlock height="40px" />
                <SkeletonBlock height="60px" />
              </div>
              <div v-else-if="stages" class="space-y-3">
                <div class="flex items-center justify-between">
                  <div>
                    <div class="text-xs text-slate-400">当前阶段</div>
                    <div class="text-lg font-semibold text-cyber-neonCyan">{{ stages.current_stage.name }}</div>
                  </div>
                  <div class="text-right">
                    <div class="text-xs text-slate-400">已进行</div>
                    <div class="text-sm">{{ stages.days_in_stage }} 天</div>
                  </div>
                </div>
                <div class="flex gap-1">
                  <div v-for="s in stages.all_stages" :key="s.id" class="flex-1 py-2 rounded text-center text-[10px]" :class="getStageClass(s)">
                    <div>{{ s.name }}</div>
                    <div class="text-xs mt-0.5">{{ s.status === 'completed' ? '✓' : s.status === 'active' ? '●' : '○' }}</div>
                  </div>
                </div>
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <div class="p-2 rounded bg-white/5">
                    <div class="text-slate-400">目标温度</div>
                    <div>{{ stages.current_stage.target_temp_min }}-{{ stages.current_stage.target_temp_max }}℃</div>
                  </div>
                  <div class="p-2 rounded bg-white/5">
                    <div class="text-slate-400">目标湿度</div>
                    <div>{{ stages.current_stage.target_humidity_min }}-{{ stages.current_stage.target_humidity_max }}%</div>
                  </div>
                </div>
              </div>
            </GlassCard>

            <GlassCard title="告警记录" class="hud h-[250px] flex flex-col">
              <div v-if="alertsLoading" class="space-y-2">
                <SkeletonBlock height="30px" v-for="i in 3" :key="i" />
              </div>
              <div v-else-if="alerts.length" class="flex-1 overflow-auto pr-1 space-y-2">
                <div v-for="alert in alerts" :key="alert.id" class="p-2 rounded-lg border text-xs" :class="getAlertClass(alert.level)">
                  <div class="flex items-center gap-1.5 mb-1">
                    <div class="h-1.5 w-1.5 rounded-full" :class="getAlertDotClass(alert.level)" />
                    <span class="font-medium">{{ alert.title }}</span>
                    <span v-if="alert.auto_action" class="ml-auto text-[9px] px-1.5 py-0.5 rounded bg-cyber-neonCyan/20 text-cyber-neonCyan">
                      已自动
                    </span>
                  </div>
                  <div class="text-slate-400 leading-tight">{{ alert.message }}</div>
                  <div class="text-[9px] text-slate-500 mt-1">{{ formatTime(alert.ts) }}</div>
                </div>
              </div>
              <div v-else class="text-center text-slate-400 py-8 text-sm">暂无告警</div>
            </GlassCard>

            <GlassCard title="SOP任务" class="hud h-[250px] flex flex-col">
              <div v-if="tasksLoading" class="space-y-2">
                <SkeletonBlock height="30px" v-for="i in 3" :key="i" />
              </div>
              <div v-else-if="tasks.length" class="flex-1 overflow-auto pr-1 space-y-2">
                <div v-for="task in tasks" :key="task.id" class="flex items-center gap-2 p-2 rounded-lg border" :class="getTaskClass(task.status)">
                  <div class="h-5 w-5 rounded flex items-center justify-center text-[10px] flex-shrink-0" :class="getTaskStatusClass(task.status)">
                    {{ task.status === 'completed' ? '✓' : task.status === 'in_progress' ? '●' : '○' }}
                  </div>
                  <div class="flex-1 min-w-0">
                    <div class="text-xs font-medium truncate">{{ task.title }}</div>
                    <div class="text-[9px] text-slate-400">{{ task.scheduled_time }}</div>
                  </div>
                  <NeonButton v-if="task.status !== 'completed'" size="xs" @click="completeTask(task.id)" :loading="completingTask === task.id">
                    完成
                  </NeonButton>
                </div>
              </div>
              <div v-else class="text-center text-slate-400 py-8 text-sm">暂无任务</div>
            </GlassCard>

            <GlassCard title="24小时历史曲线" class="hud">
              <div ref="historyChartEl" class="h-[180px]" />
            </GlassCard>

            <GlassCard title="场景推演与答辩口径" class="hud">
              <template #right>
                <div class="flex gap-2">
                  <button
                    v-for="scenario in simulationScenarios"
                    :key="scenario.key"
                    @click="activeSimulation = scenario.key"
                    class="rounded-full px-2.5 py-1 text-[10px] transition-colors"
                    :class="activeSimulation === scenario.key ? 'bg-cyber-neonCyan/20 text-cyber-neonCyan' : 'bg-white/5 text-slate-400'"
                  >
                    {{ scenario.label }}
                  </button>
                </div>
              </template>
              <div class="space-y-3">
                <div class="grid grid-cols-3 gap-2 text-xs">
                  <div v-for="item in activeSimulationCards" :key="item.label" class="rounded-lg border border-white/10 bg-white/5 p-3">
                    <div class="text-slate-400">{{ item.label }}</div>
                    <div class="mt-1 text-lg font-semibold" :class="item.color">{{ item.value }}</div>
                    <div class="mt-1 text-[10px] text-slate-500">{{ item.note }}</div>
                  </div>
                </div>
                <div class="rounded-xl border border-cyber-neonViolet/15 bg-cyber-neonViolet/5 p-4 text-xs leading-6 text-slate-300">
                  {{ activeSimulationNarrative }}
                </div>
              </div>
            </GlassCard>
          </div>
        </template>

        <div v-else class="flex-1 flex items-center justify-center">
          <div class="text-center text-slate-400">
            <div class="text-4xl mb-4">🏗️</div>
            <div class="text-lg">选择左侧大棚查看详情</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

import { getDashboardSummary, getTimeseries } from '../api/dashboard'
import { exportData as exportGreenhouseData } from '../api/export'
import { getStages, getAlerts, getTasks, completeTask as apiCompleteTask } from '../api/operations'
import GlassCard from '../components/GlassCard.vue'
import NeonButton from '../components/NeonButton.vue'
import SkeletonBlock from '../components/SkeletonBlock.vue'

const greenhouses = ref([])
const selectedId = ref(null)
const stages = ref(null)
const stagesLoading = ref(false)
const alerts = ref([])
const alertsLoading = ref(false)
const tasks = ref([])
const tasksLoading = ref(false)
const completingTask = ref(null)
const historyChartEl = ref(null)
const compareChartEl = ref(null)
const activeCompareMode = ref('adherence')
const activeSimulation = ref('stability')
let historyChart = null
let compareChart = null

const compareModes = [
  { key: 'adherence', label: '达标率' },
  { key: 'risk', label: '风险分' },
  { key: 'efficiency', label: '执行效率' }
]

const simulationScenarios = [
  { key: 'stability', label: '稳态生产' },
  { key: 'heat', label: '高温预警' },
  { key: 'teaching', label: '教学示范' }
]

const simulationMap = {
  stability: {
    narrative: '当前口径强调系统在日常生产中的稳定调控能力：参数偏差出现后先预警，再驱动灌溉/通风，最后沉淀成 SOP 复盘记录。',
    cards: [
      { label: '预计优质率', value: '91%', note: '适合展示稳定生产收益', color: 'text-cyber-neonCyan' },
      { label: '异常闭环时长', value: '6.2min', note: '监测到动作执行全链路', color: 'text-cyber-neonViolet' },
      { label: '作业规范度', value: '95%', note: 'SOP 可追溯', color: 'text-cyber-neonPink' }
    ]
  },
  heat: {
    narrative: '在高温预警场景下，可用这块解释系统如何通过阈值判断、风机联动和告警通知，把“发现晚”变成“提前干预”。',
    cards: [
      { label: '高温响应', value: '2.8min', note: '风机联动更快', color: 'text-cyber-neonCyan' },
      { label: '损耗压降', value: '-17%', note: '减少热害导致的品质波动', color: 'text-cyber-neonViolet' },
      { label: '峰值风险分', value: '39', note: '比人工巡检模式更低', color: 'text-cyber-neonPink' }
    ]
  },
  teaching: {
    narrative: '如果面向老师或评委展示产教融合，可以强调不同棚室的数据差异如何用于实验教学、案例分析和跨学科实践。',
    cards: [
      { label: '可用实验题组', value: '12组', note: '适合课程设计', color: 'text-cyber-neonCyan' },
      { label: '样本可解释性', value: '高', note: '参数变化直观', color: 'text-cyber-neonViolet' },
      { label: '答辩展示完成度', value: '96%', note: '图表和场景都完整', color: 'text-cyber-neonPink' }
    ]
  }
}

const selectedGreenhouse = computed(() => greenhouses.value.find(g => g.id === selectedId.value))
const activeSimulationCards = computed(() => simulationMap[activeSimulation.value].cards)
const activeSimulationNarrative = computed(() => simulationMap[activeSimulation.value].narrative)

const compareSummary = computed(() => {
  if (!greenhouses.value.length) return []
  const sorted = [...greenhouses.value].sort((a, b) => (b.score || 0) - (a.score || 0))
  const best = sorted[0]
  const weakest = sorted[sorted.length - 1]
  const avg = Math.round(greenhouses.value.reduce((sum, item) => sum + (item.score || 0), 0) / greenhouses.value.length)
  return [
    { label: '最佳展示棚', value: best ? `${best.name} ${best.score}%` : '-', note: '适合作为答辩实时演示主案例', color: 'text-cyber-neonCyan' },
    { label: '重点优化棚', value: weakest ? `${weakest.name} ${weakest.score}%` : '-', note: '便于说明系统如何处理低达标场景', color: 'text-cyber-neonPink' },
    { label: '多棚平均表现', value: `${avg}%`, note: '可直接支撑“标准化复制”叙事', color: 'text-cyber-neonViolet' }
  ]
})

onMounted(async () => {
  await loadGreenhouses()
  if (greenhouses.value.length) await selectGreenhouse(greenhouses.value[0].id)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  historyChart?.dispose()
  compareChart?.dispose()
  window.removeEventListener('resize', handleResize)
})

watch(activeCompareMode, async () => {
  await nextTick()
  renderCompareChart()
})

async function loadGreenhouses() {
  try {
    const summary = await getDashboardSummary()
    greenhouses.value = summary.top_risk.map(g => ({
      ...g,
      latest: summary.latest_by_greenhouse[g.id],
      score: g.curve_adherence_pct,
      area: 180 + g.id * 20
    }))
    await nextTick()
    renderCompareChart()
  } catch (e) {
    console.error(e)
  }
}

async function selectGreenhouse(id) {
  selectedId.value = id
  await loadDetails(id)
}

async function loadDetails(greenhouseId) {
  stagesLoading.value = true
  alertsLoading.value = true
  tasksLoading.value = true
  try {
    const [st, al, ta, ts] = await Promise.all([
      getStages(greenhouseId),
      getAlerts(greenhouseId),
      getTasks(greenhouseId),
      getTimeseries(greenhouseId)
    ])
    stages.value = st
    alerts.value = al
    tasks.value = ta
    await renderHistoryChart(ts)
  } catch (e) {
    console.error(e)
  } finally {
    stagesLoading.value = false
    alertsLoading.value = false
    tasksLoading.value = false
  }
}

async function renderHistoryChart(ts) {
  await nextTick()
  if (!historyChartEl.value) return
  if (!historyChart) historyChart = echarts.init(historyChartEl.value)
  const x = ts.points.map(p => p.ts.slice(11, 16))
  const temp = ts.points.map(p => p.air_temp_c)
  const hum = ts.points.map(p => p.air_humidity_pct)
  historyChart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 35, right: 10, top: 10, bottom: 20 },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: x, axisLine: { lineStyle: { color: 'rgba(148,163,184,.35)' } }, axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 9 } },
    yAxis: { type: 'value', axisLine: { show: false }, splitLine: { lineStyle: { color: 'rgba(148,163,184,.12)' } }, axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 9 } },
    series: [
      { name: '温度', type: 'line', smooth: true, data: temp, showSymbol: false, lineStyle: { width: 2, color: '#8B5CF6' } },
      { name: '湿度', type: 'line', smooth: true, data: hum, showSymbol: false, lineStyle: { width: 2, color: '#EC4899' } }
    ]
  })
}

function renderCompareChart() {
  if (!compareChartEl.value || !greenhouses.value.length) return
  if (!compareChart) compareChart = echarts.init(compareChartEl.value)
  const labels = greenhouses.value.map(g => g.name)
  const values = greenhouses.value.map((g) => {
    if (activeCompareMode.value === 'risk') return g.risk_score
    if (activeCompareMode.value === 'efficiency') return Math.min(99, Math.round((g.curve_adherence_pct || 0) * 0.72 + 18))
    return g.score || 0
  })
  compareChart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 35, right: 12, top: 20, bottom: 25 },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: labels, axisLine: { lineStyle: { color: 'rgba(148,163,184,.35)' } }, axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 } },
    yAxis: { type: 'value', splitLine: { lineStyle: { color: 'rgba(148,163,184,.12)' } }, axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 } },
    series: [
      {
        name: activeCompareMode.value,
        type: activeCompareMode.value === 'efficiency' ? 'line' : 'bar',
        smooth: true,
        data: values,
        showSymbol: activeCompareMode.value === 'efficiency',
        barWidth: 24,
        itemStyle: { color: activeCompareMode.value === 'risk' ? '#EC4899' : '#8B5CF6', borderRadius: [6, 6, 0, 0] },
        lineStyle: { width: 3, color: '#22D3EE' },
        areaStyle: activeCompareMode.value === 'efficiency' ? { color: 'rgba(34,211,238,.10)' } : undefined
      }
    ]
  })
}

async function completeTask(taskId) {
  completingTask.value = taskId
  try {
    await apiCompleteTask(taskId)
    await loadDetails(selectedId.value)
  } finally {
    completingTask.value = null
  }
}

function batchIrrigate() {
  window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'info', msg: '已切换为比赛演示口径：展示多棚批量灌溉能力' } }))
}

function exportData() {
  if (!selectedId.value) {
    window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'error', msg: '请先选择要导出的棚室' } }))
    return
  }
  exportGreenhouseData(selectedId.value, 'xlsx')
    .then(() => {
      window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'success', msg: `已导出 ${selectedGreenhouse.value?.name || ''} 的历史数据` } }))
    })
    .catch(() => {
      window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'error', msg: '数据导出失败，请稍后重试' } }))
    })
}

function refreshData() {
  selectGreenhouse(selectedId.value)
}

function goSettings() {
  window.dispatchEvent(new CustomEvent('app-toast', { detail: { type: 'info', msg: '建议前往成果与参数中心补充答辩口径' } }))
}

function handleResize() {
  historyChart?.resize()
  compareChart?.resize()
}

function getStageClass(s) {
  if (s.status === 'completed') return 'bg-cyber-neonViolet/20 border border-cyber-neonViolet/30 text-cyber-neonViolet'
  if (s.status === 'active') return 'bg-cyber-neonCyan/30 border border-cyber-neonCyan/50 text-cyber-neonCyan'
  return 'bg-white/5 border border-white/10 text-slate-400'
}

function getAlertClass(level) {
  if (level === 'critical') return 'border-cyber-neonPink/20 bg-cyber-neonPink/5'
  if (level === 'warning') return 'border-cyber-neonViolet/20 bg-cyber-neonViolet/5'
  return 'border-cyber-neonCyan/20 bg-cyber-neonCyan/5'
}

function getAlertDotClass(level) {
  if (level === 'critical') return 'bg-cyber-neonPink animate-pulse'
  if (level === 'warning') return 'bg-cyber-neonViolet'
  return 'bg-cyber-neonCyan'
}

function getTaskClass(status) {
  if (status === 'completed') return 'border-cyber-neonCyan/20 bg-cyber-neonCyan/5'
  if (status === 'in_progress') return 'border-cyber-neonViolet/20 bg-cyber-neonViolet/5'
  return 'border-white/10 bg-white/5'
}

function getTaskStatusClass(status) {
  if (status === 'completed') return 'bg-cyber-neonCyan/20 text-cyber-neonCyan'
  if (status === 'in_progress') return 'bg-cyber-neonViolet/20 text-cyber-neonViolet'
  return 'bg-white/10 text-slate-400'
}

function formatTime(ts) {
  const date = new Date(ts)
  return date.toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar { width: 4px; }
.custom-scrollbar::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); }
.custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(139, 92, 246, 0.3); border-radius: 10px; }
.custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(139, 92, 246, 0.5); }
</style>
