<script setup lang="ts">
import { computed, onMounted, onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Lenis from 'lenis'
import SiteHeader from './components/SiteHeader.vue'
import SiteFooter from './components/SiteFooter.vue'
import WhatsAppButton from './components/WhatsAppButton.vue'
import MouseFollower from './components/MouseFollower.vue'
import { useCatalog } from './stores'

const route = useRoute()
const catalog = useCatalog()
const isAdmin = computed(() => route.path.startsWith('/admin'))
const isAdminApp = computed(() => isAdmin.value && route.path !== '/admin/login')

let lenis: Lenis | null = null

onMounted(() => {
  catalog.load().catch(() => {})
  lenis = new Lenis({ lerp: 0.08 })
  function raf(time: number) {
    lenis?.raf(time)
    requestAnimationFrame(raf)
  }
  requestAnimationFrame(raf)
})

watch(
  () => route.fullPath,
  () => lenis?.scrollTo(0, { immediate: true }),
)

onUnmounted(() => lenis?.destroy())
</script>

<template>
  <div class="flex min-h-svh flex-col">
    <MouseFollower v-if="!isAdminApp" />
    <SiteHeader v-if="!isAdmin" />
    <div class="flex flex-1 flex-col">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </div>
    <SiteFooter v-if="!isAdmin" />
    <WhatsAppButton v-if="!isAdmin" />
  </div>
</template>
