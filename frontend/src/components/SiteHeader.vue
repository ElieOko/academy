<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Menu, X } from '@lucide/vue'

const { t, locale } = useI18n()
const route = useRoute()
const open = ref(false)
const scrolled = ref(false)

if (typeof window !== 'undefined') {
  window.addEventListener('scroll', () => {
    scrolled.value = window.scrollY > 24
  })
}

const links = computed(() => [
  { to: '/', label: t('nav.home') },
  { to: '/a-propos', label: t('nav.about') },
  { to: '/formations', label: t('nav.programs') },
  { to: '/calendrier', label: t('nav.calendar') },
  { to: '/entreprises', label: t('nav.enterprise') },
  { to: '/actualites', label: t('nav.news') },
  { to: '/contact', label: t('nav.contact') },
])

const overHero = computed(() => route.path === '/' && !scrolled.value)

function toggleLocale() {
  locale.value = locale.value === 'fr' ? 'en' : 'fr'
  localStorage.setItem('academy_locale', String(locale.value))
}

watch(
  () => route.path,
  () => {
    open.value = false
  },
)
</script>

<template>
  <header
    class="fixed inset-x-0 top-0 z-40 transition-all duration-300"
    :class="overHero ? 'bg-transparent' : 'bg-cream/90 shadow-sm backdrop-blur-md'"
  >
    <div class="container-page flex h-[72px] items-center justify-between gap-4">
      <RouterLink to="/" class="flex items-center gap-2.5">
        <span
          class="flex h-9 w-9 items-center justify-center rounded-lg font-display text-lg font-semibold"
          :class="overHero ? 'bg-gold text-navy' : 'bg-navy text-gold'"
        >A</span>
        <span class="leading-tight">
          <span class="block font-display text-[17px] font-semibold" :class="overHero ? 'text-white' : 'text-navy'">Acad’Emy</span>
          <span class="block text-[10px] tracking-[0.14em] uppercase" :class="overHero ? 'text-white/70' : 'text-mute'">Learn. Build. Lead.</span>
        </span>
      </RouterLink>

      <nav class="hidden items-center gap-6 lg:flex">
        <RouterLink
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          class="text-[13px] transition hover:text-gold"
          :class="overHero ? 'text-white/85' : 'text-navy/80'"
        >
          {{ l.label }}
        </RouterLink>
      </nav>

      <div class="flex items-center gap-2">
        <button
          type="button"
          class="rounded-full border px-3 py-1.5 text-[11px] font-semibold tracking-wide"
          :class="overHero ? 'border-white/30 text-white' : 'border-navy/15 text-navy'"
          @click="toggleLocale"
        >
          {{ locale === 'fr' ? 'Français / English' : 'English / Français' }}
        </button>
        <RouterLink to="/inscription" class="btn btn-gold hidden px-4 py-2 text-xs md:inline-flex">
          {{ t('cta.enroll') }}
        </RouterLink>
        <button class="lg:hidden" :class="overHero ? 'text-white' : 'text-navy'" @click="open = !open">
          <X v-if="open" :size="22" />
          <Menu v-else :size="22" />
        </button>
      </div>
    </div>

    <div v-if="open" class="border-t border-white/10 bg-navy lg:hidden">
      <nav class="container-page flex flex-col py-4">
        <RouterLink v-for="l in links" :key="l.to" :to="l.to" class="py-2.5 text-white/90">
          {{ l.label }}
        </RouterLink>
        <RouterLink to="/inscription" class="btn btn-gold mt-3">{{ t('cta.enroll') }}</RouterLink>
      </nav>
    </div>
  </header>
</template>
