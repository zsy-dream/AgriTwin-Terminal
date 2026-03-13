<template>
  <div class="min-h-screen bg-cyber noise relative overflow-hidden">
    <div
      class="pointer-events-none absolute inset-0 opacity-70"
      style="background-image: var(--grid); background-size: 44px 44px"
    />

    <div class="relative mx-auto max-w-7xl px-4 py-6 md:px-6 pb-24 md:pb-6">
      <header class="mb-6 flex items-center justify-between rounded-[22px] border border-white/10 bg-[#0c1328]/70 px-4 py-3 backdrop-blur-xl md:px-5">
        <div class="flex items-center gap-3">
          <div class="relative h-10 w-10">
            <div class="absolute inset-0 rounded-xl bg-gradient-to-br from-cyber-neonViolet/40 to-cyber-neonPink/30 blur-md animate-pulseGlow" />
            <div
              class="relative h-10 w-10 rounded-xl border border-cyber-border bg-cyber-panel shadow-neon flex items-center justify-center"
            >
              <svg class="h-6 w-6 text-cyber-neonCyan" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M12 2L4 7v10c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V7l-8-5z" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 7v10" stroke-linecap="round"/>
                <path d="M12 12c2-2 4-2 6 0s2 4 0 6" stroke-linecap="round"/>
                <circle cx="12" cy="9" r="1.5" fill="currentColor"/>
              </svg>
            </div>
          </div>
          <div class="leading-tight hidden sm:block">
            <div class="text-sm text-slate-300/80">Plant Factory</div>
            <div class="text-lg font-semibold tracking-wide bg-gradient-to-r from-cyber-neonCyan via-cyber-neonViolet to-cyber-neonPink bg-clip-text text-transparent">智汇大棚</div>
            <div class="text-[10px] text-slate-500">互联网+比赛展示版</div>
          </div>
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-2 rounded-[18px] border border-white/8 bg-white/5 px-2 py-2">
          <NeonButton variant="ghost" @click="go('/dashboard')">驾驶舱</NeonButton>
          <NeonButton variant="ghost" @click="go('/greenhouses')">棚群</NeonButton>
          <NeonButton variant="ghost" @click="go('/settings')">设置</NeonButton>
          <div class="w-px h-6 bg-white/10 mx-1" />
          <button @click="logout" class="p-2 rounded-xl text-slate-400 hover:text-cyber-neonPink hover:bg-white/5 transition-colors">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
          </button>
        </div>

        <!-- Mobile User Menu -->
        <div class="md:hidden flex items-center gap-2">
          <button @click="showMobileMenu = !showMobileMenu" class="p-2 rounded-xl bg-white/5 border border-white/10 shadow-neon">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </header>

      <!-- Mobile Menu Dropdown -->
      <div v-if="showMobileMenu" class="md:hidden mb-4 p-4 rounded-[22px] bg-[#0c1328]/90 border border-white/10 space-y-2 backdrop-blur-xl">
        <button @click="go('/dashboard'); showMobileMenu = false" class="w-full p-3 rounded-xl text-left hover:bg-white/5">驾驶舱</button>
        <button @click="go('/greenhouses'); showMobileMenu = false" class="w-full p-3 rounded-xl text-left hover:bg-white/5">棚群管理</button>
        <button @click="go('/settings'); showMobileMenu = false" class="w-full p-3 rounded-xl text-left hover:bg-white/5">系统设置</button>
        <div class="border-t border-white/10 pt-2">
          <button @click="logout" class="w-full p-3 rounded-xl text-left text-cyber-neonPink hover:bg-cyber-neonPink/10">退出登录</button>
        </div>
      </div>

      <main>
        <router-view />
      </main>
    </div>

    <!-- Mobile Bottom Navigation -->
    <div class="md:hidden fixed bottom-0 left-0 right-0 bg-ink/95 backdrop-blur-xl border-t border-white/10 safe-area-pb shadow-[0_-12px_40px_rgba(0,0,0,.35)]">
      <div class="flex justify-around items-center h-16">
        <button @click="go('/dashboard')" class="flex flex-col items-center gap-1 p-2" :class="$route.path === '/dashboard' ? 'text-cyber-neonCyan' : 'text-slate-400'">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
          </svg>
          <span class="text-[10px]">驾驶舱</span>
        </button>
        <button @click="go('/greenhouses')" class="flex flex-col items-center gap-1 p-2" :class="$route.path === '/greenhouses' ? 'text-cyber-neonCyan' : 'text-slate-400'">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span class="text-[10px]">棚群</span>
        </button>
        <button @click="go('/settings')" class="flex flex-col items-center gap-1 p-2" :class="$route.path === '/settings' ? 'text-cyber-neonCyan' : 'text-slate-400'">
          <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
          </svg>
          <span class="text-[10px]">设置</span>
        </button>
      </div>
    </div>

    <ToastHost />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

import NeonButton from '../components/NeonButton.vue'
import ToastHost from '../components/ToastHost.vue'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const showMobileMenu = ref(false)

function go(path) {
  router.push(path)
}

async function logout() {
  await authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
:global(.bg-cyber) {
  --grid: linear-gradient(rgba(139, 92, 246, 0.12) 1px, transparent 1px),
    linear-gradient(90deg, rgba(236, 72, 153, 0.1) 1px, transparent 1px);
}

.safe-area-pb {
  padding-bottom: env(safe-area-inset-bottom, 0px);
}
</style>
