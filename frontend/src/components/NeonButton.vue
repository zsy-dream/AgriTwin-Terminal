<template>
  <button
    :disabled="disabled || loading"
    class="group relative inline-flex items-center justify-center rounded-[16px] px-4 py-2.5 text-sm font-semibold transition duration-300 disabled:cursor-not-allowed disabled:opacity-60"
    :class="cls"
    :style="{ '--sx': sx + '%' }"
    @click="onClick"
  >
    <span
      class="pointer-events-none absolute inset-0 rounded-xl2 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
      :class="hoverGlow"
    />

    <span
      class="pointer-events-none absolute -inset-px rounded-xl2 opacity-70 blur-sm"
      :class="ringGlow"
    />

    <span
      class="pointer-events-none absolute inset-0 overflow-hidden rounded-xl2 opacity-0 group-hover:opacity-100"
    >
      <span
        class="absolute left-0 top-0 h-full w-1/2 -translate-x-[140%] bg-gradient-to-r from-transparent via-white/25 to-transparent"
        style="transform: translateX(var(--sx, -140%));"
        :class="shimmerClass"
      />
    </span>

    <span class="relative flex items-center gap-2">
      <span v-if="loading" class="relative h-4 w-4">
        <span class="absolute inset-0 rounded-full border border-white/25" />
        <span
          class="absolute inset-0 rounded-full border-2 border-cyber-neonCyan/70 border-t-transparent animate-spin"
        />
      </span>
      <slot />
    </span>
  </button>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'

const props = defineProps({
  variant: { type: String, default: 'primary' },
  disabled: { type: Boolean, default: false },
  loading: { type: Boolean, default: false }
})

const emit = defineEmits(['click'])

const sx = ref(-140)
let t = null

onMounted(() => {
  t = setInterval(() => {
    sx.value = sx.value >= 140 ? -140 : sx.value + 8
  }, 70)
})

onUnmounted(() => {
  if (t) clearInterval(t)
})

function onClick(e) {
  if (props.disabled || props.loading) return
  emit('click', e)
}

const cls = computed(() => {
  const base =
    'select-none active:translate-y-[1px] active:scale-[0.99] focus:outline-none focus-visible:ring-2 focus-visible:ring-cyber-neonViolet/60'

  if (props.variant === 'ghost') {
    return [
      base,
      'border border-white/10 bg-white/5 text-slate-100 shadow-neon hover:border-cyber-neonViolet/30 hover:bg-white/8 hover:shadow-neonStrong'
    ]
  }

  return [
    base,
    'border border-cyber-neonViolet/25 bg-gradient-to-b from-cyber-neonViolet/65 to-cyber-neonPink/40 text-white shadow-neon hover:shadow-neonStrong'
  ]
})

const ringGlow = computed(() =>
  props.variant === 'ghost'
    ? 'bg-gradient-to-r from-cyber-neonViolet/15 via-cyber-neonPink/10 to-cyber-neonCyan/10'
    : 'bg-gradient-to-r from-cyber-neonViolet/25 via-cyber-neonPink/18 to-cyber-neonCyan/15'
)

const hoverGlow = computed(() =>
  props.variant === 'ghost'
    ? 'bg-gradient-to-r from-cyber-neonViolet/10 via-cyber-neonPink/8 to-cyber-neonCyan/8'
    : 'bg-gradient-to-r from-cyber-neonViolet/18 via-cyber-neonPink/12 to-cyber-neonCyan/12'
)

const shimmerClass = computed(() => 'animate-shimmer')
</script>

<style scoped></style>
