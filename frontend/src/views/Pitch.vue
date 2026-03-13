<template>
  <div class="space-y-4 pb-6">
    <section class="grid grid-cols-12 gap-4">
      <GlassCard class="col-span-12 min-h-[340px]">
        <div class="flex h-full flex-col justify-between gap-6">
          <div class="flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
            <div class="max-w-4xl">
              <div class="inline-flex items-center gap-2 rounded-full border border-cyber-neonCyan/20 bg-cyber-neonCyan/10 px-3 py-1 text-xs text-cyber-neonCyan">
                互联网+一页式路演首页
              </div>
              <h1 class="mt-4 text-4xl font-semibold leading-tight md:text-5xl">
                智汇大棚
                <span class="bg-gradient-to-r from-cyber-neonCyan via-cyber-neonViolet to-cyber-neonPink bg-clip-text text-transparent">
                  高附加值作物数字孪生调控终端
                </span>
              </h1>
              <p class="mt-4 text-sm leading-7 text-slate-300/85 md:text-base">
                以高附加值作物为目标对象，围绕温湿度、土壤含水率、CO₂、pH/营养液等关键理化参数，
                构建“感知采集—数字孪生—风险预警—设备调控—SOP复盘”的全流程数字化种植解决方案。
              </p>
            </div>
            <div class="grid w-full gap-3 sm:grid-cols-2 xl:w-[360px] xl:grid-cols-1">
              <div v-for="item in quickFacts" :key="item.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="text-xs text-slate-400">{{ item.label }}</div>
                <div class="mt-1 text-2xl font-semibold" :class="item.color">{{ item.value }}</div>
                <div class="mt-1 text-[11px] text-slate-500">{{ item.note }}</div>
              </div>
            </div>
          </div>
          <div class="grid gap-3 md:grid-cols-4">
            <div v-for="item in coreBlocks" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
              <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
                <span class="text-lg">{{ item.icon }}</span>
                <span>{{ item.title }}</span>
              </div>
              <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="项目数据化总览" class="col-span-12 xl:col-span-7">
        <template #right>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="scenario in scenarios"
              :key="scenario.key"
              @click="activeScenario = scenario.key"
              class="rounded-full px-3 py-1 text-[11px] transition-colors"
              :class="activeScenario === scenario.key ? 'bg-cyber-neonViolet/20 text-cyber-neonViolet' : 'bg-white/5 text-slate-400'"
            >
              {{ scenario.label }}
            </button>
          </div>
        </template>
        <div class="space-y-4">
          <div class="grid gap-3 md:grid-cols-4">
            <div v-for="item in activeScenarioStats" :key="item.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
              <div class="text-[11px] text-slate-400">{{ item.label }}</div>
              <div class="mt-2 text-2xl font-semibold" :class="item.color">{{ item.value }}</div>
              <div class="mt-1 text-[10px] text-slate-500">{{ item.note }}</div>
            </div>
          </div>
          <div class="grid gap-4 lg:grid-cols-[1.3fr_0.7fr]">
            <div class="rounded-xl border border-white/10 bg-white/5 p-4">
              <div class="mb-3 flex items-center justify-between">
                <div class="text-sm font-medium text-slate-100">阶段化成果曲线</div>
                <div class="text-[11px] text-slate-500">{{ activeScenarioMeta.period }}</div>
              </div>
              <div ref="pitchChartEl" class="h-[260px]" />
            </div>
            <div class="space-y-3">
              <div class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 text-sm font-medium text-slate-100">落地推进进度</div>
                <div class="space-y-3">
                  <div v-for="item in activeScenarioMilestones" :key="item.label">
                    <div class="mb-1 flex items-center justify-between text-[11px]">
                      <span class="text-slate-400">{{ item.label }}</span>
                      <span class="text-slate-200">{{ item.value }}%</span>
                    </div>
                    <div class="h-2 rounded-full bg-white/10">
                      <div class="h-2 rounded-full bg-gradient-to-r from-cyber-neonViolet to-cyber-neonCyan" :style="{ width: `${item.value}%` }" />
                    </div>
                  </div>
                </div>
              </div>
              <div class="rounded-xl border border-cyber-neonCyan/15 bg-cyber-neonCyan/5 p-4">
                <div class="text-sm font-medium text-slate-100">当前展示口径</div>
                <div class="mt-2 text-xs leading-6 text-slate-300">{{ activeScenarioMeta.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
      <GlassCard title="技术壁垒拆解" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="item in moatBlocks" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="text-xs" :class="item.color">{{ item.score }}/100</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
            <div class="mt-3 h-2 rounded-full bg-white/10">
              <div class="h-2 rounded-full" :class="item.barClass" :style="{ width: `${item.score}%` }" />
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="项目亮点与特色标签" class="col-span-12 xl:col-span-6">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in featureHighlights" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full px-2 py-1 text-[10px]" :class="item.badgeClass">{{ item.badge }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="为什么这个项目适合互联网+" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="item in competitionFit" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="答辩开场推荐话术" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="speech in speeches" :key="speech.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">{{ speech.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ speech.text }}</div>
          </div>
        </div>
      </GlassCard>
      <GlassCard title="路演页面入口" class="col-span-12 xl:col-span-6">
        <div class="grid gap-3 md:grid-cols-2">
          <button
            v-for="entry in entries"
            :key="entry.path"
            @click="go(entry.path)"
            class="rounded-xl border border-white/10 bg-white/5 p-4 text-left transition-all hover:border-cyber-neonViolet/30 hover:bg-white/8"
          >
            <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
              <span class="text-lg">{{ entry.icon }}</span>
              <span>{{ entry.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ entry.desc }}</div>
          </button>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="评委视角下的核心卖点" class="col-span-12 xl:col-span-8">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in judgeSellingPoints" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
      <GlassCard title="路演流程建议" class="col-span-12 xl:col-span-4">
        <div class="space-y-3">
          <div v-for="(step, index) in flow" :key="step.title" class="flex gap-3 rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-cyber-neonViolet/20 text-sm font-semibold text-cyber-neonViolet">
              {{ index + 1 }}
            </div>
            <div>
              <div class="text-sm font-medium text-slate-100">{{ step.title }}</div>
              <div class="mt-1 text-xs leading-6 text-slate-400">{{ step.desc }}</div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>
  </div>
</template>

<script setup>
import * as echarts from 'echarts'
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import GlassCard from '../components/GlassCard.vue'

const router = useRouter()
const activeScenario = ref('pilot')
const pitchChartEl = ref(null)
let pitchChart = null

function go(path) {
  router.push(path)
}

const quickFacts = [
  { label: '项目定位', value: '高值作物数字调控', note: '面向高附加值作物种植场景', color: 'text-cyber-neonCyan' },
  { label: '技术路线', value: '感知 + 孪生 + 调控', note: '从看数据走向做决策', color: 'text-cyber-neonViolet' },
  { label: '比赛优势', value: '专业性 + 展示性', note: '兼顾理化口径与可视化表达', color: 'text-cyber-neonPink' },
  { label: '落地路径', value: '单棚验证 → 园区复制', note: '适合互联网+评委理解', color: 'text-slate-100' }
]

const coreBlocks = [
  { icon: '🧪', title: '理化参数表达', desc: '突出温湿度、CO₂、pH/营养液等化学相关指标，契合化学院学生专业背景。' },
  { icon: '📊', title: '可视化完整', desc: '具备驾驶舱、成果页、商业页和一页式路演首页，适合答辩展示节奏。' },
  { icon: '🚨', title: '闭环调控逻辑', desc: '从异常识别到动作执行，再到SOP复盘，形成完整数字农业闭环。' },
  { icon: '💼', title: '商业叙事清晰', desc: '能同时回答“技术怎么做”和“项目如何推广、如何落地”的问题。' }
]

const scenarios = [
  { key: 'pilot', label: '校内验证棚' },
  { key: 'demo', label: '园区示范棚' },
  { key: 'scale', label: '复制推广期' }
]

const scenarioDataMap = {
  pilot: {
    period: '近6个月模拟数据',
    desc: '突出“项目可做成”，适合答辩开场展示从实验验证到系统成型的增长逻辑。',
    stats: [
      { label: '环境达标率', value: '92%', note: '重点参数稳定落在目标带', color: 'text-cyber-neonCyan' },
      { label: '人工巡检减少', value: '38%', note: '异常识别前移', color: 'text-cyber-neonViolet' },
      { label: '单棚预警响应', value: '4.6min', note: '从发现到动作下发', color: 'text-cyber-neonPink' },
      { label: 'SOP执行率', value: '95%', note: '作业记录可追溯', color: 'text-slate-100' }
    ],
    milestones: [
      { label: '采集链路稳定性', value: 88 },
      { label: '数字孪生拟合度', value: 84 },
      { label: '控制策略可解释性', value: 91 }
    ],
    chart: { x: ['1月', '2月', '3月', '4月', '5月', '6月'], quality: [72, 78, 83, 86, 91, 94], efficiency: [58, 63, 69, 77, 82, 87] }
  },
  demo: {
    period: '近2季度示范数据',
    desc: '突出“项目能落地”，适合展示多棚协同和示范基地的标准化复制能力。',
    stats: [
      { label: '多棚协同数', value: '8座', note: '统一监测与任务流转', color: 'text-cyber-neonCyan' },
      { label: '风险下降', value: '31%', note: '高温/缺水异常减少', color: 'text-cyber-neonViolet' },
      { label: '优质果率提升', value: '19%', note: '高值作物品质更稳定', color: 'text-cyber-neonPink' },
      { label: '老师/农户满意度', value: '96%', note: '更易教学与示范', color: 'text-slate-100' }
    ],
    milestones: [
      { label: '示范棚标准化程度', value: 93 },
      { label: '自动调控覆盖率', value: 79 },
      { label: '成果展示完整度', value: 96 }
    ],
    chart: { x: ['Q1', 'Q2', 'Q3', 'Q4'], quality: [68, 74, 82, 89], efficiency: [61, 70, 78, 86] }
  },
  scale: {
    period: '复制期年度测算',
    desc: '突出“项目可推广”，适合说明营收空间、标准产品化和区域复制潜力。',
    stats: [
      { label: '年服务棚数', value: '50+', note: '按园区复制测算', color: 'text-cyber-neonCyan' },
      { label: '设备运维效率', value: '+27%', note: '统一巡检和远程协同', color: 'text-cyber-neonViolet' },
      { label: '综合增收', value: '18-24%', note: '品质提升叠加损耗下降', color: 'text-cyber-neonPink' },
      { label: '平台复购率', value: '81%', note: '数据沉淀形成黏性', color: 'text-slate-100' }
    ],
    milestones: [
      { label: '区域复制准备度', value: 86 },
      { label: '商业化交付能力', value: 82 },
      { label: '服务标准件成熟度', value: 88 }
    ],
    chart: { x: ['2026', '2027', '2028', '2029'], quality: [76, 83, 88, 93], efficiency: [66, 74, 81, 90] }
  }
}

const activeScenarioData = computed(() => scenarioDataMap[activeScenario.value])
const activeScenarioStats = computed(() => activeScenarioData.value.stats)
const activeScenarioMilestones = computed(() => activeScenarioData.value.milestones)
const activeScenarioMeta = computed(() => ({ period: activeScenarioData.value.period, desc: activeScenarioData.value.desc }))

const speeches = [
  { title: '30秒版本', text: '我们的项目聚焦高附加值作物种植，通过多源传感、数字孪生和设备联动，实现关键环境参数的精准调控，提升高值作物种植的稳定性与标准化水平。' },
  { title: '1分钟版本', text: '传统高值作物种植高度依赖经验，容易出现参数波动不可视、异常处置滞后和标准复制困难的问题。我们构建了一个集实时感知、风险预警、设备调控、SOP管理和数据复盘于一体的数字孪生调控终端，既能展示技术能力，也具备落地推广价值。' }
]

const featureHighlights = [
  { title: '高值场景聚焦', badge: '强场景', badgeClass: 'bg-cyber-neonCyan/15 text-cyber-neonCyan', desc: '不是泛农业平台，而是聚焦环境敏感、收益更高的高附加值作物，问题更真实，价值更突出。' },
  { title: '监测到调控闭环', badge: '强技术', badgeClass: 'bg-cyber-neonViolet/15 text-cyber-neonViolet', desc: '把采集、预警、动作、复盘串成一套完整逻辑，比单纯看板更像真正可落地的解决方案。' },
  { title: '理化参数特色鲜明', badge: '强专业', badgeClass: 'bg-cyber-neonPink/15 text-cyber-neonPink', desc: '将温湿度、CO₂、pH/营养液等指标纳入答辩表达，更容易体现化学院学生的专业辨识度。' },
  { title: '展示完成度高', badge: '强路演', badgeClass: 'bg-white/10 text-slate-200', desc: '具备路演首页、成果页、驾驶舱、商业页和参数页，现场展示链路完整，比赛观感强。' }
]

const competitionFit = [
  { title: '符合互联网+重点方向', desc: '同时覆盖智慧农业、乡村振兴、数字技术应用和产教融合，题目方向天然适配比赛评审逻辑。' },
  { title: '能同时讲技术和落地', desc: '既有数字孪生、预警调控等技术点，也能讲园区复制、教学示范和数据服务等应用场景。' },
  { title: '有辨识度而不空泛', desc: '相较普通管理系统，本项目对象更明确、参数更专业、可视化更完整，更容易让评委记住。' }
]

const entries = [
  { path: '/showcase', icon: '⚡', title: '项目亮点', desc: '快速讲清项目定位、技术路线和价值输出。' },
  { path: '/business', icon: '💰', title: '商业答辩', desc: '说明商业模式、团队优势、推广路径与壁垒。' },
  { path: '/dashboard', icon: '🖥️', title: '实时驾驶舱', desc: '展示系统实时监测、预警和控制能力。' },
  { path: '/settings', icon: '🧾', title: '成果与参数中心', desc: '用表格、指标和阶段口径体现专业严谨性。' }
]

const judgeSellingPoints = [
  { title: '不是普通物联网看板', desc: '不是停留在数据展示，而是把监测、预警、控制、复盘四段链路串起来。' },
  { title: '更适合高值农业场景', desc: '聚焦高附加值作物，单棚收益高，环境控制价值更明显。' },
  { title: '跨学科特色鲜明', desc: '化学与软件结合，使项目兼具理化检测逻辑和数字系统实现能力。' },
  { title: '易于比赛传播', desc: '页面结构清晰，图表、表格、业务表达完整，适合路演、答辩和成果展示。' }
]

const flow = [
  { title: '先展示路演首页', desc: '用一页完成项目总览，快速抓住评委注意力。' },
  { title: '再切项目亮点页', desc: '讲技术逻辑、参数体系、模拟成果和应用价值。' },
  { title: '接商业答辩页', desc: '说明商业模式、推广路径和团队优势。' },
  { title: '最后看驾驶舱', desc: '证明系统不仅会讲故事，也具备真实交互和数据链路。' }
]

const moatBlocks = [
  { title: '理化参数模型', desc: '把化学相关环境指标转成可监测、可解释、可干预的统一参数口径。', score: 91, color: 'text-cyber-neonCyan', barClass: 'bg-gradient-to-r from-cyber-neonCyan to-cyber-neonViolet' },
  { title: '多棚数据闭环', desc: '不是单点设备堆叠，而是采集、预警、调控、任务复盘的一体化链路。', score: 88, color: 'text-cyber-neonViolet', barClass: 'bg-gradient-to-r from-cyber-neonViolet to-cyber-neonPink' },
  { title: '比赛展示能力', desc: '具备路演首页、驾驶舱、参数中心和商业答辩页，叙事与数据都完整。', score: 95, color: 'text-cyber-neonPink', barClass: 'bg-gradient-to-r from-cyber-neonPink to-cyber-neonCyan' }
]

function renderPitchChart() {
  if (!pitchChartEl.value) return
  if (!pitchChart) pitchChart = echarts.init(pitchChartEl.value, null, { renderer: 'canvas' })
  const current = activeScenarioData.value.chart
  pitchChart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 35, right: 20, top: 30, bottom: 25 },
    tooltip: { trigger: 'axis' },
    legend: {
      data: ['品质稳定度', '运营效率'],
      right: 0,
      top: 0,
      textStyle: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    xAxis: {
      type: 'category',
      data: current.x,
      axisLine: { lineStyle: { color: 'rgba(148,163,184,.35)' } },
      axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      min: 40,
      max: 100,
      splitLine: { lineStyle: { color: 'rgba(148,163,184,.12)' } },
      axisLabel: { color: 'rgba(226,232,240,.7)', fontSize: 10 }
    },
    series: [
      { name: '品质稳定度', type: 'line', smooth: true, data: current.quality, symbolSize: 7, lineStyle: { width: 2, color: '#22D3EE' }, areaStyle: { color: 'rgba(34,211,238,.10)' } },
      { name: '运营效率', type: 'bar', barWidth: 18, data: current.efficiency, itemStyle: { borderRadius: [6, 6, 0, 0], color: '#8B5CF6' } }
    ]
  })
}

function handleResize() {
  pitchChart?.resize()
}

onMounted(async () => {
  await nextTick()
  renderPitchChart()
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  pitchChart?.dispose()
})

watch(activeScenario, async () => {
  await nextTick()
  renderPitchChart()
})
</script>
