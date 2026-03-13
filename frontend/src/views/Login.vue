<template>
  <div class="grid min-h-[calc(100vh-120px)] grid-cols-12 gap-4 items-center">
    <GlassCard class="col-span-12 lg:col-span-7 min-h-[520px]">
      <div class="flex h-full flex-col justify-between gap-6">
        <div class="space-y-4">
          <div class="inline-flex items-center gap-2 rounded-full border border-cyber-neonCyan/20 bg-cyber-neonCyan/10 px-3 py-1 text-xs text-cyber-neonCyan">
            互联网+答辩登录入口
          </div>
          <div>
            <h1 class="text-3xl font-semibold leading-tight md:text-4xl">
              智汇大棚
              <span class="bg-gradient-to-r from-cyber-neonCyan via-cyber-neonViolet to-cyber-neonPink bg-clip-text text-transparent">
                高附加值作物数字孪生调控终端
              </span>
            </h1>
            <p class="mt-3 max-w-2xl text-sm leading-7 text-slate-300/85">
              面向藏红花、人参、名贵兰花、铁皮石斛等高附加值作物，构建“感知采集—数字孪生—异常预警—SOP执行—经营复盘”一体化调控平台。
            </p>
          </div>
        </div>

        <div class="grid gap-3 md:grid-cols-3">
          <div v-for="item in highlights" :key="item.title" class="rounded-xl border border-white/10 bg-white/5 p-4">
            <div class="mb-2 flex items-center gap-2 text-sm font-medium text-slate-100">
              <span class="text-lg">{{ item.icon }}</span>
              <span>{{ item.title }}</span>
            </div>
            <div class="text-xs leading-6 text-slate-400">{{ item.desc }}</div>
          </div>
        </div>
      </div>
    </GlassCard>

    <GlassCard class="col-span-12 lg:col-span-5">
      <div class="mb-6 text-center">
        <div class="text-3xl mb-2">🪪</div>
        <h2 class="text-xl font-semibold">演示系统登录</h2>
        <p class="text-sm text-slate-400 mt-1">进入驾驶舱、路演页与商业答辩页</p>
      </div>

      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-xs text-slate-400 mb-1">用户名</label>
          <input
            v-model="form.username"
            type="text"
            class="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-sm focus:border-cyber-neonViolet/50 focus:outline-none transition-colors"
            placeholder="admin / operator / viewer"
            required
          />
        </div>

        <div>
          <label class="block text-xs text-slate-400 mb-1">密码</label>
          <input
            v-model="form.password"
            type="password"
            class="w-full px-3 py-2 rounded-xl bg-white/5 border border-white/10 text-sm focus:border-cyber-neonViolet/50 focus:outline-none transition-colors"
            placeholder="请输入密码"
            required
          />
        </div>

        <div v-if="error" class="p-2 rounded-lg bg-cyber-neonPink/10 border border-cyber-neonPink/20 text-xs text-cyber-neonPink">
          {{ error }}
        </div>

        <NeonButton type="submit" :loading="authStore.loading" class="w-full">
          进入演示系统
        </NeonButton>
      </form>

      <div class="mt-5 rounded-xl border border-white/10 bg-white/5 p-4 text-xs">
        <div class="mb-2 text-sm font-medium text-slate-100">测试账号</div>
        <div class="space-y-1 text-slate-400">
          <p>管理员：`admin / admin123`</p>
          <p>操作员：`operator / operator123`</p>
          <p>观察员：`viewer / viewer123`</p>
        </div>
      </div>
    </GlassCard>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import GlassCard from '../components/GlassCard.vue'
import NeonButton from '../components/NeonButton.vue'

const highlights = [
  { icon: '📡', title: '多源感知', desc: '统一采集温湿度、土壤水分、CO₂ 与作物阶段信息。' },
  { icon: '🧠', title: '数字孪生', desc: '将理想生长目标带与实时数据对照，形成偏差识别能力。' },
  { icon: '📈', title: '比赛展示友好', desc: '集成项目亮点页、商业答辩页和驾驶舱，适合路演开场展示。' }
]

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const error = ref('')

const handleLogin = async () => {
  error.value = ''
  const result = await authStore.login(form.username, form.password)
  if (result.success) {
    router.push('/dashboard')
  } else {
    error.value = result.message
  }
}
</script>
