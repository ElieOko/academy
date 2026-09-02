<script setup lang="ts">
import { RouterLink, RouterView, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const router = useRouter()
const links = [
  { to: '/admin', label: 'overview' },
  { to: '/admin/formations', label: 'programs' },
  { to: '/admin/sessions', label: 'sessions' },
  { to: '/admin/inscriptions', label: 'enrollments' },
  { to: '/admin/actualites', label: 'news' },
  { to: '/admin/temoignages', label: 'testimonials' },
  { to: '/admin/entreprises', label: 'enterprise' },
  { to: '/admin/messages', label: 'messages' },
  { to: '/admin/parametres', label: 'settings' },
]

function logout() {
  localStorage.removeItem('academy_token')
  router.push('/admin/login')
}
</script>

<template>
  <div class="min-h-screen bg-cream md:flex">
    <aside class="bg-navy p-6 text-white md:w-60 md:shrink-0">
      <RouterLink to="/" class="flex items-center gap-2">
        <span class="flex h-9 w-9 items-center justify-center overflow-hidden rounded-lg bg-white">
          <img src="/images/academy-mark.jpg" alt="" class="h-20 w-20 object-contain transition-transform scale-150" />
        </span>
        <span class="font-display text-xl text-gold">ACAD’EMY</span>
      </RouterLink>
      <nav class="mt-8 flex flex-col gap-1 text-sm">
        <RouterLink
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          class="rounded-lg px-3 py-2 text-white/75 hover:bg-white/10 hover:text-white"
          :class="($route.path === l.to || (l.to !== '/admin' && $route.path.startsWith(l.to))) && '!bg-white/15 !text-gold'"
        >
          {{ t(`admin.${l.label}`) }}
        </RouterLink>
      </nav>
      <button class="mt-8 text-xs text-white/50 hover:text-white" @click="logout">{{ t('admin.out') }}</button>
    </aside>
    <div class="min-w-0 flex-1 p-6 md:p-10">
      <RouterView />
    </div>
  </div>
</template>
