<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const x = ref(-120)
const y = ref(-120)
const tx = ref(-120)
const ty = ref(-120)
const hovering = ref(false)
const enabled = ref(false)
let raf = 0

function isInteractive(el: EventTarget | null) {
  if (!(el instanceof Element)) return false
  return Boolean(el.closest('a, button, input, textarea, select, label, [role="button"]'))
}

function onMove(e: MouseEvent) {
  x.value = e.clientX
  y.value = e.clientY
  hovering.value = isInteractive(e.target)
}

function tick() {
  tx.value += (x.value - tx.value) * 0.16
  ty.value += (y.value - ty.value) * 0.16
  raf = requestAnimationFrame(tick)
}

onMounted(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches
  const coarse = window.matchMedia('(pointer: coarse)').matches
  enabled.value = !reduce && !coarse
  if (!enabled.value) return
  window.addEventListener('mousemove', onMove, { passive: true })
  raf = requestAnimationFrame(tick)
})

onUnmounted(() => {
  window.removeEventListener('mousemove', onMove)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div v-if="enabled" class="pointer-events-none fixed inset-0 z-[80] hidden md:block" aria-hidden="true">
    <div class="mouse-spot" :style="{ left: `${x}px`, top: `${y}px` }" />
    <div
      class="mouse-ring"
      :class="hovering ? 'is-hover' : ''"
      :style="{ transform: `translate3d(${tx}px, ${ty}px, 0)` }"
    />
  </div>
</template>
