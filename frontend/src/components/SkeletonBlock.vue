<template>
  <div class="relative overflow-hidden rounded-xl bg-white/5" :style="{ height, width }">
    <div class="absolute inset-0 -translate-x-[120%] animate-shimmer bg-gradient-to-r from-transparent via-white/10 to-transparent" />
  </div>
</template>

<script setup>
defineProps({
  height: { type: String, default: '14px' },
  width: { type: String, default: '100%' }
})
</script>
