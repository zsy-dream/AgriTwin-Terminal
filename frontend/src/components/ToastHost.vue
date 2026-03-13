<template>
  <div class="fixed bottom-4 right-4 z-50 flex w-[320px] flex-col gap-2">
    <transition-group name="toast" tag="div">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="neon-border hud rounded-xl2 border border-cyber-border bg-cyber-panel/70 px-4 py-3 shadow-neon"
      >
        <div class="flex items-start gap-3">
          <div
            class="mt-0.5 h-2.5 w-2.5 rounded-full"
            :class="t.type === 'error' ? 'bg-cyber-neonPink' : t.type === 'info' ? 'bg-cyber-neonCyan' : 'bg-cyber-neonViolet'"
          />
          <div class="flex-1">
            <div class="text-xs text-slate-300/70">{{ t.type.toUpperCase() }}</div>
            <div class="text-sm text-slate-100">{{ t.msg }}</div>
          </div>
          <button class="text-slate-300/70 hover:text-slate-100" @click="remove(t.id)">
            ✕
          </button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

const toasts = ref([])

function push({ type = 'info', msg = '' }) {
  const id = `${Date.now()}-${Math.random()}`
  toasts.value = [{ id, type, msg }, ...toasts.value].slice(0, 4)
  setTimeout(() => remove(id), 2800)
}

function remove(id) {
  toasts.value = toasts.value.filter((x) => x.id !== id)
}

function handler(e) {
  push(e.detail || {})
}

onMounted(() => window.addEventListener('app-toast', handler))
onUnmounted(() => window.removeEventListener('app-toast', handler))
</script>

<style scoped>
.toast-enter-active,
.toast-leave-active {
  transition: all 220ms ease;
}

.toast-enter-from,
.toast-leave-to {
  opacity: 0;
  transform: translateY(10px);
}
</style>
