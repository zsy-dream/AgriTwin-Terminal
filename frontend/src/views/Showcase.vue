<template>
  <div class="space-y-4 pb-6">
    <section class="grid grid-cols-12 gap-4">
      <GlassCard class="col-span-12 lg:col-span-8 min-h-[280px]">
        <div class="flex h-full flex-col justify-between gap-6">
          <div class="space-y-4">
            <div class="inline-flex items-center gap-2 rounded-full border border-cyber-neonCyan/20 bg-cyber-neonCyan/10 px-3 py-1 text-xs text-cyber-neonCyan">
              互联网+答辩展示模式
            </div>
            <div class="space-y-3">
              <h1 class="text-3xl font-semibold leading-tight md:text-4xl">
                智汇大棚
                <span class="bg-gradient-to-r from-cyber-neonCyan via-cyber-neonViolet to-cyber-neonPink bg-clip-text text-transparent">
                  高附加值作物数字孪生调控终端
                </span>
              </h1>
              <p class="max-w-3xl text-sm leading-7 text-slate-300/85 md:text-base">
                面向藏红花、人参、铁皮石斛、名贵兰花等高价值作物，构建“感知采集—数字孪生—风险预警—SOP执行—经营复盘”一体化闭环，
                让传统设施农业从经验驱动升级为数据驱动、模型驱动和标准驱动。
              </p>
            </div>

            <div class="grid gap-3 md:grid-cols-3">
              <div v-for="item in scientificHighlights" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
                <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
                  <span class="text-lg">{{ item.icon }}</span>
                  <span>{{ item.title }}</span>
                </div>
                <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
              </div>
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
            <div v-for="card in heroCards" :key="card.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
              <div class="mb-2 text-xs text-slate-400">{{ card.label }}</div>
              <div class="text-2xl font-semibold" :class="card.color">{{ card.value }}</div>
              <div class="mt-1 text-xs text-slate-500">{{ card.hint }}</div>
            </div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="项目竞争力" class="col-span-12 lg:col-span-4">
        <div class="space-y-3">
          <div v-for="item in advantages" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 flex items-center gap-2 text-sm font-medium">
              <span>{{ item.icon }}</span>
              <span>{{ item.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
        <div class="mt-3 rounded-xl border border-cyber-neonViolet/15 bg-cyber-neonViolet/5 p-4">
          <div class="mb-3 text-sm font-medium text-slate-100">评委高频关注点</div>
          <div class="space-y-2">
            <div v-for="focus in judgeFocus" :key="focus.label" class="flex items-center justify-between text-xs">
              <span class="text-slate-400">{{ focus.label }}</span>
              <span class="rounded-full px-2 py-1" :class="focus.cls">{{ focus.value }}</span>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="传统种植 vs 数字调控 总板" class="col-span-12">
        <div class="grid gap-4 xl:grid-cols-2">
          <div class="rounded-xl border border-cyber-neonPink/20 bg-cyber-neonPink/5 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">传统经验种植</div>
              <span class="rounded-full bg-cyber-neonPink/15 px-2 py-1 text-[10px] text-cyber-neonPink">痛点侧</span>
            </div>
            <div class="space-y-3">
              <div v-for="item in traditionalPainPoints" :key="item.title" class="rounded-lg border border-white/10 bg-white/5 p-3">
                <div class="mb-1 text-sm font-medium text-slate-100">{{ item.title }}</div>
                <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
              </div>
            </div>
          </div>
          <div class="rounded-xl border border-cyber-neonCyan/20 bg-cyber-neonCyan/5 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">智汇大棚数字调控</div>
              <span class="rounded-full bg-cyber-neonCyan/15 px-2 py-1 text-[10px] text-cyber-neonCyan">解决方案侧</span>
            </div>
            <div class="space-y-3">
              <div v-for="item in digitalAdvantages" :key="item.title" class="rounded-lg border border-white/10 bg-white/5 p-3">
                <div class="mb-1 text-sm font-medium text-slate-100">{{ item.title }}</div>
                <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="成果图板与答辩证据" class="col-span-12 xl:col-span-7">
        <div class="grid gap-3 md:grid-cols-3">
          <div v-for="item in resultBoards" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="text-xs" :class="item.color">{{ item.delta }}</span>
            </div>
            <div class="text-2xl font-semibold" :class="item.color">{{ item.value }}</div>
            <div class="mt-1 text-[11px] text-slate-500">{{ item.note }}</div>
            <div class="mt-3 h-2 rounded-full bg-white/10">
              <div class="h-2 rounded-full" :class="item.barClass" :style="{ width: `${item.progress}%` }" />
            </div>
          </div>
        </div>
        <div class="mt-4 grid gap-3 md:grid-cols-2">
          <div v-for="item in comparisonPanels" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full bg-white/5 px-2 py-1 text-[10px] text-slate-400">{{ item.tag }}</span>
            </div>
            <div class="space-y-2">
              <div v-for="row in item.rows" :key="row.label">
                <div class="mb-1 flex items-center justify-between text-[11px]">
                  <span class="text-slate-400">{{ row.label }}</span>
                  <span class="text-slate-200">{{ row.value }}</span>
                </div>
                <div class="h-2 rounded-full bg-white/10">
                  <div class="h-2 rounded-full bg-gradient-to-r from-cyber-neonViolet to-cyber-neonCyan" :style="{ width: `${row.progress}%` }" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="项目里程碑路线图" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="(item, index) in roadmapBoards" :key="item.title" class="flex gap-3 rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-cyber-neonViolet/20 text-sm font-semibold text-cyber-neonViolet">
              {{ index + 1 }}
            </div>
            <div class="min-w-0">
              <div class="flex items-center justify-between gap-3">
                <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
                <span class="text-[10px] text-slate-500">{{ item.phase }}</span>
              </div>
              <div class="mt-1 text-xs leading-6 text-slate-400">{{ item.desc }}</div>
              <div class="mt-2 text-[11px] text-cyber-neonCyan">{{ item.result }}</div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="核心能力矩阵" class="col-span-12 xl:col-span-7">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in capabilities" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full bg-white/5 px-2 py-1 text-[10px] text-slate-400">{{ item.tag }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="答辩推荐演示链路" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="(step, index) in demoSteps" :key="step.title" class="flex gap-3 rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full bg-cyber-neonViolet/20 text-sm font-semibold text-cyber-neonViolet">
              {{ index + 1 }}
            </div>
            <div>
              <div class="text-sm font-medium">{{ step.title }}</div>
              <div class="mt-1 text-xs leading-6 text-slate-400">{{ step.desc }}</div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="技术路线与闭环逻辑" class="col-span-12">
        <div class="grid gap-3 xl:grid-cols-5">
          <div v-for="(item, index) in pipeline" :key="item.title" class="relative rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-3 flex items-center justify-between">
              <div class="flex h-8 w-8 items-center justify-center rounded-full bg-cyber-neonCyan/15 text-sm font-semibold text-cyber-neonCyan">
                {{ index + 1 }}
              </div>
              <span class="text-lg">{{ item.icon }}</span>
            </div>
            <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="mt-2 text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="关键环境参数与化学检测口径" class="col-span-12 xl:col-span-7">
        <div class="overflow-x-auto">
          <table class="w-full min-w-[720px] text-left text-xs">
            <thead>
              <tr class="border-b border-white/10 text-slate-400">
                <th class="px-3 py-3 font-medium">指标</th>
                <th class="px-3 py-3 font-medium">目标区间</th>
                <th class="px-3 py-3 font-medium">检测意义</th>
                <th class="px-3 py-3 font-medium">调控动作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="row in chemistryIndicators" :key="row.name" class="border-b border-white/5">
                <td class="px-3 py-3 text-slate-200">
                  <div class="flex items-center gap-2">
                    <span class="text-base">{{ row.icon }}</span>
                    <span>{{ row.name }}</span>
                  </div>
                </td>
                <td class="px-3 py-3 text-cyber-neonCyan">{{ row.range }}</td>
                <td class="px-3 py-3 text-slate-400">{{ row.meaning }}</td>
                <td class="px-3 py-3 text-slate-300">{{ row.action }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </GlassCard>

      <GlassCard title="阶段性成果模拟数据" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="metric in mockMetrics" :key="metric.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ metric.label }}</div>
              <span class="text-xs" :class="metric.trendClass">{{ metric.trend }}</span>
            </div>
            <div class="flex items-end justify-between gap-3">
              <div>
                <div class="text-2xl font-semibold" :class="metric.valueClass">{{ metric.value }}</div>
                <div class="mt-1 text-[11px] text-slate-500">{{ metric.note }}</div>
              </div>
              <div class="w-28">
                <div class="mb-1 flex items-center justify-between text-[10px] text-slate-500">
                  <span>完成度</span>
                  <span>{{ metric.progress }}%</span>
                </div>
                <div class="h-2 rounded-full bg-white/10">
                  <div class="h-2 rounded-full bg-gradient-to-r from-cyber-neonViolet to-cyber-neonCyan" :style="{ width: `${metric.progress}%` }" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="预期价值输出" class="col-span-12 lg:col-span-5">
        <div class="space-y-3">
          <div v-for="item in values" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 text-sm font-medium">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="比赛表达关键词" class="col-span-12 lg:col-span-4">
        <div class="flex flex-wrap gap-2">
          <span
            v-for="tag in pitchTags"
            :key="tag"
            class="rounded-full border border-cyber-neonCyan/20 bg-cyber-neonCyan/10 px-3 py-1.5 text-xs text-cyber-neonCyan"
          >
            {{ tag }}
          </span>
        </div>
        <div class="mt-4 rounded-xl border border-cyber-neonViolet/20 bg-cyber-neonViolet/5 p-4 text-xs leading-6 text-slate-300">
          建议答辩时先讲“高价值作物种植痛点”，再演示实时驾驶舱、异常预警、SOP任务闭环，最后落到提质增效、标准复制和区域推广。
        </div>
      </GlassCard>

      <GlassCard title="当前系统数据映射" class="col-span-12 lg:col-span-3">
        <div class="space-y-3 text-xs">
          <div class="rounded-xl bg-white/5 p-3">
            <div class="text-slate-400">重点监控棚</div>
            <div class="mt-1 text-base font-semibold text-cyber-neonCyan">{{ topGreenhouseName }}</div>
          </div>
          <div class="rounded-xl bg-white/5 p-3">
            <div class="text-slate-400">当前最高风险值</div>
            <div class="mt-1 text-base font-semibold text-cyber-neonPink">{{ topRiskScore }}</div>
          </div>
          <div class="rounded-xl bg-white/5 p-3">
            <div class="text-slate-400">在线感知状态</div>
            <div class="mt-1 text-base font-semibold" :class="summary.total_greenhouses ? 'text-cyber-neonCyan' : 'text-slate-400'">
              {{ summary.total_greenhouses ? '数据接入正常' : '等待数据' }}
            </div>
          </div>
          <div class="rounded-xl bg-white/5 p-3">
            <div class="text-slate-400">理论叙事完整度</div>
            <div class="mt-1 text-base font-semibold text-cyber-neonViolet">{{ storyScore }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="面向互联网+路演的表达模板" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="block in speechBlocks" :key="block.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
              <span>{{ block.icon }}</span>
              <span>{{ block.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ block.text }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="答辩风险点与应对" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="risk in defenseRisks" :key="risk.q" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">Q：{{ risk.q }}</div>
            <div class="text-xs leading-6 text-slate-400">A：{{ risk.a }}</div>
          </div>
        </div>
      </GlassCard>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'

import GlassCard from '../components/GlassCard.vue'
import { getDashboardSummary } from '../api/dashboard'

const summary = ref({
  total_greenhouses: 0,
  top_risk: [],
  latest_by_greenhouse: {}
})

const heroCards = computed(() => {
  const total = summary.value.total_greenhouses || 0
  const activeAlerts = summary.value.top_risk.reduce((sum, item) => sum + (item.active_alerts_count || 0), 0)
  const avgAdherence = summary.value.top_risk.length
    ? Math.round(summary.value.top_risk.reduce((sum, item) => sum + (item.curve_adherence_pct || 0), 0) / summary.value.top_risk.length)
    : 0

  return [
    { label: '联网棚室', value: `${total}座`, hint: '多棚统一监测与协同调控', color: 'text-cyber-neonCyan' },
    { label: '实时告警', value: `${activeAlerts}条`, hint: '异常预警直达业务现场', color: 'text-cyber-neonPink' },
    { label: '环境达标率', value: `${avgAdherence}%`, hint: '数字孪生曲线拟合水平', color: 'text-cyber-neonViolet' },
    { label: '标准作业', value: 'SOP闭环', hint: '任务执行可追踪、可复盘', color: 'text-slate-100' }
  ]
})

const topGreenhouseName = computed(() => summary.value.top_risk?.[0]?.name || '暂无')
const topRiskScore = computed(() => summary.value.top_risk?.[0]?.risk_score ?? '--')
const storyScore = computed(() => {
  const score = 78 + Math.min(12, summary.value.total_greenhouses * 2)
  return `${score}/100`
})

const scientificHighlights = [
  { icon: '🧪', title: '理化指标联动', desc: '将温湿度、土壤含水率、CO₂浓度与生长阶段参数联动展示，表达更符合化学与分析测试逻辑。' },
  { icon: '📐', title: '参数边界明确', desc: '每个指标给出控制区间、异常阈值和响应动作，避免“数据很多但结论不严谨”的展示问题。' },
  { icon: '🔬', title: '适合实验室叙事', desc: '可以用“检测—判定—反馈控制”的科研表达方式讲清系统价值，便于化学院学生答辩。' }
]

const advantages = [
  { icon: '🎯', title: '聚焦高附加值作物', desc: '面向高客单价、高环境敏感度作物，单棚增益空间更大，商业落地更清晰。' },
  { icon: '🧠', title: '数字孪生+规则联动', desc: '不只采数看图，而是把阶段目标、风险识别、设备动作和SOP管理连成一套闭环。' },
  { icon: '📈', title: '易于比赛讲故事', desc: '能够清晰呈现“痛点—方案—效果—推广”逻辑，适合路演、答辩和成果展示。' }
]

const traditionalPainPoints = [
  { title: '依赖人工经验', desc: '环境判断主要依赖种植经验，参数偏差难以及时量化，管理稳定性弱。' },
  { title: '异常发现滞后', desc: '问题常在人工巡检后才暴露，高温、缺水、湿度异常容易错过最佳干预窗口。' },
  { title: '标准难复制', desc: '不同棚室、不同人员的操作口径不统一，优秀经验难沉淀成标准流程。' }
]

const digitalAdvantages = [
  { title: '数据连续感知', desc: '关键环境参数实时采集、趋势可视，让问题从“事后发现”转为“过程监测”。' },
  { title: '预警到调控闭环', desc: '异常出现后可以快速完成识别、提示、动作执行和任务留痕，缩短响应链路。' },
  { title: 'SOP可沉淀复制', desc: '把种植过程中的规则、阈值和处置流程沉淀下来，支持多棚复制和示范推广。' }
]

const judgeFocus = [
  { label: '创新性', value: '数字孪生+设施农业融合', cls: 'bg-cyber-neonCyan/10 text-cyber-neonCyan' },
  { label: '应用性', value: '多棚可复制部署', cls: 'bg-cyber-neonViolet/10 text-cyber-neonViolet' },
  { label: '专业性', value: '参数区间与检测逻辑完整', cls: 'bg-cyber-neonPink/10 text-cyber-neonPink' },
  { label: '展示性', value: '图表、表格、故事线齐全', cls: 'bg-white/10 text-slate-300' }
]

const capabilities = [
  { title: '多源环境感知', tag: '感知层', desc: '统一采集温度、湿度、土壤水分、光照等关键环境指标，支撑实时感知与历史追踪。' },
  { title: '数字孪生驾驶舱', tag: '可视化层', desc: '通过实时曲线、3D温室、棚群排行和生长进度，建立全局态势认知。' },
  { title: '风险预警与处置', tag: '决策层', desc: '对异常环境和告警进行分级提示，支持确认闭环与自动化动作延展。' },
  { title: 'SOP标准执行', tag: '执行层', desc: '将阶段任务、人工处置和设备控制纳入统一任务链，减少经验依赖。' }
]

const pipeline = [
  { icon: '📡', title: '环境感知', desc: '温度、湿度、土壤水分、CO₂与光照等指标进行实时采集与上传。' },
  { icon: '🧮', title: '数据建模', desc: '依据作物生长阶段建立指标目标带，形成数字孪生的理想曲线与偏差模型。' },
  { icon: '🚨', title: '风险识别', desc: '对超限波动、趋势偏移和设备异常进行分级判定并触发预警。' },
  { icon: '⚙️', title: '调控执行', desc: '联动灌溉、通风、遮阳等动作，实现人工控制与自动控制协同。' },
  { icon: '📚', title: '复盘优化', desc: '沉淀日志、任务和导出数据，为种植策略优化与规模复制提供依据。' }
]

const chemistryIndicators = [
  { icon: '🌡️', name: '空气温度', range: '20–25 ℃', meaning: '决定代谢速率与蒸腾强度，过高易诱发胁迫，过低影响生长速率。', action: '联动通风、加热与遮阳' },
  { icon: '💧', name: '空气湿度', range: '65–75 %RH', meaning: '影响气孔开闭与病害风险，是维持组织含水状态的重要参数。', action: '联动雾化、通风与除湿' },
  { icon: '🌱', name: '土壤含水率', range: '30–45 %', meaning: '反映根际供水状态，过低导致水分胁迫，过高影响根系供氧。', action: '联动灌溉阀与排水策略' },
  { icon: '🌫️', name: 'CO₂浓度', range: '800–1200 ppm', meaning: '与光合作用速率直接相关，是高附加值作物品质调控的重要变量。', action: '联动补碳与通风换气' },
  { icon: '⚗️', name: 'pH/营养液口径', range: 'pH 5.8–6.5', meaning: '便于在答辩中体现化学检测能力，说明离子吸收与营养平衡的控制逻辑。', action: '联动配方校正与巡检复核' }
]

const mockMetrics = [
  { label: '目标环境稳定性', value: '91.3%', trend: '↑ 6.2%', trendClass: 'text-cyber-neonCyan', valueClass: 'text-cyber-neonCyan', note: 'mock：近7日关键参数落入目标带比例', progress: 91 },
  { label: '人工巡检替代率', value: '63%', trend: '↑ 18%', trendClass: 'text-cyber-neonViolet', valueClass: 'text-cyber-neonViolet', note: 'mock：数字化监测减少重复巡棚次数', progress: 63 },
  { label: '异常处置时效', value: '< 3 min', trend: '↓ 54%', trendClass: 'text-cyber-neonPink', valueClass: 'text-cyber-neonPink', note: 'mock：预警到动作下发平均耗时', progress: 88 }
]

const resultBoards = [
  { title: '环境稳定提升', value: '91.3%', delta: '+6.2%', note: '关键参数进入目标带比例', progress: 91, color: 'text-cyber-neonCyan', barClass: 'bg-gradient-to-r from-cyber-neonCyan to-cyber-neonViolet' },
  { title: '优质果率提升', value: '+18.7%', delta: '+4.8%', note: '高值作物品质稳定度提升', progress: 82, color: 'text-cyber-neonViolet', barClass: 'bg-gradient-to-r from-cyber-neonViolet to-cyber-neonPink' },
  { title: '异常处置提速', value: '<3min', delta: '-54%', note: '从告警到动作执行耗时', progress: 88, color: 'text-cyber-neonPink', barClass: 'bg-gradient-to-r from-cyber-neonPink to-cyber-neonCyan' }
]

const comparisonPanels = [
  {
    title: '传统经验种植 vs 数字调控',
    tag: '效果对比',
    rows: [
      { label: '参数可视化程度', value: '34% → 93%', progress: 93 },
      { label: '异常提前发现率', value: '41% → 86%', progress: 86 },
      { label: 'SOP执行留痕', value: '12% → 95%', progress: 95 }
    ]
  },
  {
    title: '单棚验证 vs 多棚复制',
    tag: '推广对比',
    rows: [
      { label: '监测覆盖棚数', value: '1 → 8', progress: 80 },
      { label: '标准化程度', value: '58% → 89%', progress: 89 },
      { label: '答辩展示完整度', value: '72% → 96%', progress: 96 }
    ]
  }
]

const roadmapBoards = [
  { title: '校内验证棚搭建', phase: '阶段一', desc: '完成关键传感器接入、环境曲线可视化和基础告警联动。', result: '形成可展示的原型闭环。' },
  { title: '示范棚场景打磨', phase: '阶段二', desc: '补齐 SOP 任务、阶段参数和多棚协同逻辑，让演示更像真实系统。', result: '形成比赛可演示版本。' },
  { title: '园区复制与推广', phase: '阶段三', desc: '沉淀标准交付包、参数模板和成果复盘面板，支撑区域推广。', result: '形成可复制商业化路径。' }
]

const demoSteps = [
  { title: '先看项目亮点页', desc: '用1分钟讲清目标对象、核心能力、商业价值和大赛关键词。' },
  { title: '切入驾驶舱', desc: '展示实时环境曲线、系统状态、活跃告警和数字孪生温室。' },
  { title: '进入棚群管理', desc: '说明多棚统一管理、阶段差异、任务执行和数据导出能力。' },
  { title: '收束到落地价值', desc: '强调标准复制、降本增效、农技服务和区域产业升级空间。' }
]

const values = [
  { title: '生产价值', desc: '降低环境调控滞后和人工巡检强度，提升高价值作物稳定产出与品质一致性。' },
  { title: '经营价值', desc: '沉淀种植数据资产，为品控溯源、农资服务、技术托管和园区运营提供基础。' },
  { title: '推广价值', desc: '具备“单棚验证—棚群复制—园区推广”的扩张路径，适合校地合作与产业示范。' }
]

const pitchTags = ['高价值作物', '数字孪生', '设施农业', '精准调控', '风险预警', 'SOP标准化', '多棚协同', '可复制推广']

const speechBlocks = [
  { icon: '①', title: '问题定义', text: '高附加值作物对温湿度、土壤含水率和CO₂浓度高度敏感，传统经验种植存在参数波动不可视、异常处置滞后和标准复制困难等问题。' },
  { icon: '②', title: '解决方案', text: '项目以传感器采集为基础，以数字孪生模型为核心，以SOP任务链和设备控制为执行抓手，形成“监测—分析—决策—执行—复盘”闭环。' },
  { icon: '③', title: '应用前景', text: '适用于校内科研温室、合作社示范棚和高值作物园区，可逐步延伸至技术服务、数据托管和区域示范推广。' }
]

const defenseRisks = [
  { q: '为什么你们的项目不是普通环境监测？', a: '因为系统不止做数据展示，还把阶段目标、告警判定、设备联动和任务闭环串起来，强调数字孪生和执行反馈。' },
  { q: 'mock 数据会不会显得不真实？', a: '展示时可明确说明“部分经营成效指标为模拟推演，用于表达商业场景；实时监测、曲线、告警与导出链路为系统真实功能”。' },
  { q: '化学院学生做这个项目的优势是什么？', a: '可以从理化指标判定、营养液/根际环境理解、检测逻辑构建和实验设计严谨性上体现跨学科优势。' }
]

onMounted(async () => {
  try {
    summary.value = await getDashboardSummary()
  } catch (error) {
    console.error(error)
  }
})
</script>
