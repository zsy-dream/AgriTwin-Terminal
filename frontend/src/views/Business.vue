<template>
  <div class="space-y-4 pb-6">
    <section class="grid grid-cols-12 gap-4">
      <GlassCard class="col-span-12 lg:col-span-8 min-h-[260px]">
        <div class="flex h-full flex-col justify-between gap-5">
          <div class="space-y-4">
            <div class="inline-flex items-center gap-2 rounded-full border border-cyber-neonPink/20 bg-cyber-neonPink/10 px-3 py-1 text-xs text-cyber-neonPink">
              互联网+商业模式与落地答辩页
            </div>
            <div>
              <h1 class="text-3xl font-semibold leading-tight md:text-4xl">
                从“单棚控制”到
                <span class="bg-gradient-to-r from-cyber-neonCyan via-cyber-neonViolet to-cyber-neonPink bg-clip-text text-transparent">
                  区域高值农业数字服务平台
                </span>
              </h1>
              <p class="mt-3 max-w-3xl text-sm leading-7 text-slate-300/85 md:text-base">
                项目不仅提供数字孪生监测与调控终端，还可延伸为数据服务、农技托管、园区示范与教学科研协同平台，具备“设备+系统+服务”复合型商业化潜力。
              </p>
            </div>
          </div>
          <div class="grid grid-cols-2 gap-3 md:grid-cols-4">
            <div v-for="card in summaryCards" :key="card.label" class="rounded-xl border border-white/10 bg-white/5 p-4">
              <div class="mb-2 text-xs text-slate-400">{{ card.label }}</div>
              <div class="text-2xl font-semibold" :class="card.color">{{ card.value }}</div>
              <div class="mt-1 text-[11px] text-slate-500">{{ card.note }}</div>
            </div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="评委最关心什么" class="col-span-12 lg:col-span-4">
        <div class="space-y-3">
          <div v-for="item in judgePoints" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 flex items-center gap-2 text-sm font-medium text-slate-100">
              <span>{{ item.icon }}</span>
              <span>{{ item.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="项目特色与差异化优势" class="col-span-12 xl:col-span-6">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in differentiationPoints" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full px-2 py-1 text-[10px]" :class="item.badgeClass">{{ item.badge }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="为什么评委会记住我们" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="item in memoryPoints" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="创新四象限" class="col-span-12 xl:col-span-7">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="item in innovationQuadrants" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full px-2 py-1 text-[10px]" :class="item.badgeClass">{{ item.badge }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="团队竞争力" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="item in teamBoards" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="text-xs" :class="item.color">{{ item.value }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
            <div class="mt-3 h-2 rounded-full bg-white/10">
              <div class="h-2 rounded-full" :class="item.barClass" :style="{ width: `${item.progress}%` }" />
            </div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="商业模式" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="item in businessModel" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center justify-between">
              <div class="text-sm font-medium text-slate-100">{{ item.title }}</div>
              <span class="rounded-full bg-white/5 px-2 py-1 text-[10px] text-slate-400">{{ item.tag }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="创新点拆解" class="col-span-12 xl:col-span-4">
        <div class="space-y-3">
          <div v-for="item in innovations" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="团队优势" class="col-span-12 xl:col-span-3">
        <div class="space-y-3">
          <div v-for="item in teamAdvantages" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-1 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>
    </section>

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="应用场景与客户路径" class="col-span-12 xl:col-span-7">
        <div class="grid gap-3 md:grid-cols-2">
          <div v-for="scene in applicationScenes" :key="scene.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
              <span>{{ scene.icon }}</span>
              <span>{{ scene.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ scene.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="推广路线" class="col-span-12 xl:col-span-5">
        <div class="space-y-3">
          <div v-for="(step, index) in roadmap" :key="step.title" class="flex gap-3 rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="flex h-8 w-8 items-center justify-center rounded-full bg-cyber-neonCyan/15 text-sm font-semibold text-cyber-neonCyan">
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

    <section class="grid grid-cols-12 gap-4">
      <GlassCard title="壁垒与可持续优势" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="item in moats" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">{{ item.title }}</div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </GlassCard>

      <GlassCard title="答辩高频问题应对" class="col-span-12 xl:col-span-6">
        <div class="space-y-3">
          <div v-for="item in qa" :key="item.q" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 text-sm font-medium text-slate-100">Q：{{ item.q }}</div>
            <div class="text-xs leading-6 text-slate-400">A：{{ item.a }}</div>
          </div>
        </div>
      </GlassCard>
    </section>
  </div>
</template>

<script setup>
import GlassCard from '../components/GlassCard.vue'

const summaryCards = [
  { label: '目标客户', value: '科研温室/合作社/园区', note: '从校内场景切入，向产业场景延伸', color: 'text-cyber-neonCyan' },
  { label: '交付形态', value: '设备 + 平台 + 服务', note: '软硬一体，适合项目孵化表达', color: 'text-cyber-neonViolet' },
  { label: '收入来源', value: '部署费 + 服务费', note: '兼顾一次性与持续性收入', color: 'text-cyber-neonPink' },
  { label: '推广逻辑', value: '单棚验证 → 园区复制', note: '符合互联网+评委偏好的成长路径', color: 'text-slate-100' }
]

const judgePoints = [
  { icon: '💰', title: '有没有商业闭环', desc: '不仅要说明项目能做，还要说明谁愿意买单、为什么持续使用。' },
  { icon: '🚀', title: '能不能复制推广', desc: '单点成功不是终点，关键是能否跨作物、跨棚室、跨园区复制。' },
  { icon: '🧠', title: '你们的核心壁垒是什么', desc: '要把数字孪生、理化口径与种植场景理解转化成清晰的差异化优势。' }
]

const differentiationPoints = [
  { title: '对象差异化', badge: '高价值', badgeClass: 'bg-cyber-neonCyan/15 text-cyber-neonCyan', desc: '聚焦高附加值作物而不是泛农业，单棚价值高、参数敏感度强，更容易体现数字化调控价值。' },
  { title: '链路差异化', badge: '闭环型', badgeClass: 'bg-cyber-neonViolet/15 text-cyber-neonViolet', desc: '不是停留在监测，而是形成“监测—预警—调控—SOP复盘”闭环，这是和普通平台的关键区别。' },
  { title: '专业差异化', badge: '跨学科', badgeClass: 'bg-cyber-neonPink/15 text-cyber-neonPink', desc: '把化学理化参数理解与软件系统结合，既能讲检测逻辑，也能讲系统实现。' },
  { title: '表达差异化', badge: '路演强', badgeClass: 'bg-white/10 text-slate-200', desc: '具备总览、成果、实时、商业、参数等完整表达页，项目完成度和比赛观感明显更强。' }
]

const memoryPoints = [
  { title: '不是普通后台系统', desc: '评委记住的不是“一个页面很多”，而是“这个项目能把农业参数真正变成调控闭环”。' },
  { title: '化学院学生做数字农业', desc: '跨学科标签很鲜明，容易形成“专业背景 + 技术实现 + 场景应用”的记忆点。' },
  { title: '能讲落地，也能讲未来', desc: '既可以讲单棚验证和示范棚试点，也可以讲多棚复制、园区推广和持续服务。' }
]

const innovationQuadrants = [
  { title: '技术创新', badge: '核心层', badgeClass: 'bg-cyber-neonCyan/15 text-cyber-neonCyan', desc: '把数字孪生模型、阈值规则和设备调控联动起来，不是单点功能，而是系统化能力。' },
  { title: '场景创新', badge: '应用层', badgeClass: 'bg-cyber-neonViolet/15 text-cyber-neonViolet', desc: '从泛农业转向高附加值作物，强化高敏感参数场景下的精准调控价值。' },
  { title: '专业创新', badge: '交叉层', badgeClass: 'bg-cyber-neonPink/15 text-cyber-neonPink', desc: '把化学、理化检测逻辑与软件系统结合，使项目兼具专业性和实现力。' },
  { title: '模式创新', badge: '推广层', badgeClass: 'bg-white/10 text-slate-200', desc: '从单棚验证、示范棚落地到多棚复制和数据服务，形成持续演进的商业路径。' }
]

const teamBoards = [
  { title: '跨学科适配度', value: '92/100', desc: '化学专业表达与数字系统实现相结合，能同时回答“为什么这样测”和“为什么这样做”。', progress: 92, color: 'text-cyber-neonCyan', barClass: 'bg-gradient-to-r from-cyber-neonCyan to-cyber-neonViolet' },
  { title: '答辩表达成熟度', value: '95/100', desc: '页面链路完整，项目逻辑、商业逻辑和参数逻辑都能落到直观展示中。', progress: 95, color: 'text-cyber-neonViolet', barClass: 'bg-gradient-to-r from-cyber-neonViolet to-cyber-neonPink' },
  { title: '项目推进可信度', value: '88/100', desc: '具备原型系统、示范棚叙事和园区复制路径，整体呈现更像可继续推进的项目。', progress: 88, color: 'text-cyber-neonPink', barClass: 'bg-gradient-to-r from-cyber-neonPink to-cyber-neonCyan' }
]

const businessModel = [
  { title: '智能棚室数字化部署', tag: '一次性收入', desc: '向示范基地、校内温室、合作社输出传感器接入、平台部署和可视化看板建设。' },
  { title: '种植数据服务与技术托管', tag: '持续服务', desc: '提供参数监控、阈值优化、异常复盘、SOP维护与远程运维等服务。' },
  { title: '科研与教学协同平台', tag: '场景延展', desc: '面向高校实验教学、科研课题与校地合作项目，形成教学展示与数据沉淀双重价值。' }
]

const innovations = [
  { title: '从“监测”升级为“调控闭环”', desc: '不只做环境数据展示，而是连接预警、设备动作和作业复盘。' },
  { title: '引入化学与理化参数口径', desc: '将 pH、营养液、CO₂ 等指标纳入表达体系，更符合高值作物精细化调控逻辑。' },
  { title: '面向高附加值作物场景', desc: '聚焦高客单价、高环境敏感度作物，商业价值和落地空间更清晰。' }
]

const teamAdvantages = [
  { title: '跨学科协同', desc: '化学/农业认知与软件开发结合，既能理解参数机理，也能完成系统落地。' },
  { title: '答辩表达优势', desc: '既有技术实现，也能从实验设计、理化检测、数据解释角度回答评委问题。' },
  { title: '适合校地合作', desc: '项目天然适配高校实践、创新创业、示范基地建设等场景。' }
]

const applicationScenes = [
  { icon: '🏫', title: '高校科研温室', desc: '用于实验环境管理、项目展示、数据采集与课程教学一体化。' },
  { icon: '🌿', title: '高值作物示范棚', desc: '面向藏红花、兰花、石斛、人参等高附加值作物，突出品质稳定与风险控制。' },
  { icon: '🏭', title: '园区级数字农业示范', desc: '通过多棚并行监测与协同调控，展示数字化种植的可复制价值。' },
  { icon: '🤝', title: '技术服务合作场景', desc: '可与地方农技站、合作社或企业形成设备部署与数据服务合作。' }
]

const roadmap = [
  { title: '校内验证', desc: '先完成原型系统闭环和展示效果打磨，形成可演示样板。' },
  { title: '示范棚落地', desc: '与合作基地开展单棚试点，验证参数体系、异常策略和运维流程。' },
  { title: '多棚复制', desc: '扩展到园区级场景，形成多作物、多棚室、多角色协同能力。' },
  { title: '平台化服务', desc: '沉淀数据资产与运营经验，向持续性技术托管和行业服务升级。' }
]

const moats = [
  { title: '场景壁垒', desc: '围绕高附加值作物构建的参数体系和展示语言，比通用物联网项目更贴近实际需求。' },
  { title: '数据壁垒', desc: '长期积累的环境、告警、作业与处置数据，可持续优化模型与SOP。' },
  { title: '服务壁垒', desc: '系统交付后还能延伸为培训、运维、优化和托管服务，形成长期关系。' }
]

const qa = [
  { q: '为什么客户需要你们，而不是普通传感器平台？', a: '因为我们强调高值作物场景、参数边界、预警规则和闭环执行，不只是“看数据”，而是“帮助做决策”。' },
  { q: '你们如何避免商业模式过于理想化？', a: '答辩时可以先从校内科研温室与示范棚的小场景切入，再说明复制到合作社和园区的路径，避免一步讲太大。' },
  { q: '团队优势怎样说更有说服力？', a: '突出化学院学生在理化检测、营养液理解、实验设计上的优势，再补充系统实现能力，形成跨学科亮点。' }
]
</script>
