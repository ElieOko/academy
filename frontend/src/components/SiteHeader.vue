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
    :class="overHero ? 'bg-transparent' : 'bg-cream/95 shadow-sm backdrop-blur-md'"
  >
    <div class="mx-auto flex h-[68px] max-w-[92rem] items-center gap-3 px-4 md:px-6">
      <RouterLink to="/" class="flex shrink-0 items-center gap-2.5">
        <span class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm ring-1 ring-black/5">
          <img src="/images/academy-mark.jpg" alt="" class="h-10 w-10 object-contain" />
        </span>
        <span class="font-display text-[17px] font-semibold leading-none" :class="overHero ? 'text-white' : 'text-navy'">
          Acad’Emy
        </span>
      </RouterLink>

      <nav class="hidden min-w-0 flex-1 items-center justify-end gap-x-1 lg:flex lg:justify-center lg:gap-x-2">
        <RouterLink
          v-for="l in links"
          :key="l.to"
          :to="l.to"
          class="whitespace-nowrap rounded-full px-2.5 py-1.5 text-[12.5px] font-medium transition hover:text-wine"
          :class="[
            overHero ? 'text-white/85 hover:text-gold' : 'text-navy/75',
            route.path === l.to || (l.to !== '/' && route.path.startsWith(l.to)) ? (overHero ? 'text-gold' : 'text-wine') : '',
          ]"
        >
          {{ l.label }}
        </RouterLink>
      </nav>

      <div class="ml-auto flex shrink-0 items-center gap-2 lg:ml-0">
        <button
          type="button"
          class="flex items-center rounded-full border p-0.5 text-[10px] font-semibold tracking-wide"
          :class="overHero ? 'border-white/30 text-white' : 'border-navy/15 text-navy'"
          :aria-label="locale === 'fr' ? 'Switch to English' : 'Passer en français'"
          @click="toggleLocale"
        >
          <span class="rounded-full px-2 py-1" :class="locale === 'fr' ? (overHero ? 'bg-white text-navy' : 'bg-navy text-white') : ''">FR</span>
          <span class="rounded-full px-2 py-1" :class="locale === 'en' ? (overHero ? 'bg-white text-navy' : 'bg-navy text-white') : ''">EN</span>
        </button>
        <RouterLink to="/inscription" class="btn btn-wine hidden sm:inline-flex">
          {{ t('cta.enrollShort') }}
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
        <RouterLink to="/inscription" class="btn btn-wine mt-3">{{ t('cta.enrollShort') }}</RouterLink>
      </nav>
    </div>
  </header>
</template>
