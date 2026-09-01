<script setup lang="ts">
import { onMounted, onUnmounted, ref } from 'vue'

const x = ref(-80)
const y = ref(-80)
const tx = ref(-80)
const ty = ref(-80)
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
  tx.value += (x.value - tx.value) * 0.18
  ty.value += (y.value - ty.value) * 0.18
  raf = requestAnimationFrame(tick)
}

onMounted(() => {
  enabled.value = window.matchMedia('(pointer: fine)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches
  if (!enabled.value) return
  document.documentElement.classList.add('has-mouse')
  window.addEventListener('mousemove', onMove, { passive: true })
  raf = requestAnimationFrame(tick)
})

onUnmounted(() => {
  document.documentElement.classList.remove('has-mouse')
  window.removeEventListener('mousemove', onMove)
  cancelAnimationFrame(raf)
})
</script>

<template>
  <div v-if="enabled" class="pointer-events-none fixed inset-0 z-[80] hidden md:block" aria-hidden="true">
    <div
      class="mouse-spot"
      :style="{ left: `${x}px`, top: `${y}px` }"
    />
    <div
      class="mouse-dot"
      :class="hovering ? 'scale-0' : 'scale-100'"
      :style="{ transform: `translate(${x}px, ${y}px)` }"
    />
    <div
      class="mouse-ring"
      :class="hovering ? 'is-hover' : ''"
      :style="{ transform: `translate(${tx}px, ${ty}px)` }"
    />
  </div>
</template>
