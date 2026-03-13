<template>
  <section
    class="group relative overflow-hidden rounded-[22px] border border-white/10 bg-cyber-panel/95 backdrop-blur-xl shadow-neon transition duration-300"
    :class="hoverable ? 'hover:-translate-y-1 hover:border-cyber-neonViolet/25 hover:shadow-neonStrong' : ''"
  >
    <div class="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(255,255,255,0.07),transparent_36%)] opacity-80" />
    <div class="pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-500 group-hover:opacity-100">
      <div class="absolute inset-0 bg-gradient-to-br from-cyber-neonViolet/16 via-transparent to-cyber-neonPink/14" />
      <div class="absolute -top-16 left-1/2 h-48 w-48 -translate-x-1/2 rounded-full bg-cyber-neonCyan/10 blur-2xl" />
    </div>
    <div class="relative flex h-full flex-col p-4 md:p-5">
      <header v-if="title" class="mb-4 flex items-center justify-between gap-3 border-b border-white/6 pb-3">
        <div class="flex items-center gap-2 min-w-0">
          <span class="h-2 w-2 flex-shrink-0 rounded-full bg-cyber-neonCyan/80 shadow-[0_0_10px_rgba(34,211,238,.65)]" />
          <div class="truncate text-sm font-semibold tracking-wide text-slate-100">
            {{ title }}
          </div>
        </div>
        <div v-if="$slots.right" class="text-[11px] text-slate-300/80">
          <slot name="right" />
        </div>
      </header>

      <div v-else class="mb-1" />

      <div class="flex-1 min-h-0 text-slate-200/90">
        <slot />
      </div>
    </div>

    <div class="pointer-events-none absolute inset-x-0 top-0 h-20 opacity-40">
      <div class="absolute -top-10 left-0 h-32 w-full bg-gradient-to-b from-white/10 to-transparent" />
      <div class="absolute inset-0 animate-scan bg-gradient-to-b from-transparent via-white/6 to-transparent" />
    </div>
  </section>
</template>

<script setup>
defineProps({
  title: { type: String, default: '' },
  hoverable: { type: Boolean, default: true }
})
</script>
