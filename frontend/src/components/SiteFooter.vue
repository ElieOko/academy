<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useCatalog } from '../stores'
import { loc, type Locale } from '../types'

const { t, locale } = useI18n()
const catalog = useCatalog()
const year = new Date().getFullYear()
const address = computed(() => loc(catalog.contact as never, locale.value as Locale, 'address'))

const links = computed(() => [
  { to: '/', label: t('nav.home') },
  { to: '/a-propos', label: t('nav.about') },
  { to: '/formations', label: t('nav.programs') },
  { to: '/calendrier', label: t('nav.calendar') },
  { to: '/entreprises', label: t('nav.enterprise') },
  { to: '/actualites', label: t('nav.news') },
  { to: '/contact', label: t('nav.contact') },
])
</script>

<template>
  <footer class="bg-navy text-white">
    <div class="container-page grid gap-10 py-16 md:grid-cols-4">
      <div class="md:col-span-2">
        <p class="font-display text-3xl">Acad’Emy</p>
        <p class="mt-2 text-gold">Learn. Build. Lead.</p>
        <p class="mt-4 max-w-md text-sm leading-relaxed text-white/70">
          {{ t('promiseLong') }}
        </p>
        <p class="mt-4 text-xs uppercase tracking-[0.18em] text-white/40">{{ t('parent') }}</p>
      </div>
      <div>
        <p class="eyebrow text-gold">Menu</p>
        <div class="mt-4 flex flex-col gap-2 text-sm text-white/75">
          <RouterLink v-for="l in links" :key="l.to" :to="l.to" class="hover:text-gold">{{ l.label }}</RouterLink>
        </div>
      </div>
      <div class="text-sm text-white/75">
        <p class="eyebrow text-gold">{{ t('nav.contact') }}</p>
        <p class="mt-4">{{ catalog.contact.phone }}</p>
        <p>{{ catalog.contact.email }}</p>
        <p class="mt-2">{{ address }}</p>
      </div>
    </div>
    <div class="border-t border-white/10">
      <div class="container-page flex flex-wrap items-center justify-between gap-3 py-5 text-xs text-white/45">
        <p>© {{ year }} Acad’Emy. {{ t('footer.rights') }}</p>
        <div class="flex gap-4">
          <RouterLink to="/confidentialite">{{ t('cta.privacy') }}</RouterLink>
          <RouterLink to="/admin/login">{{ t('footer.admin') }}</RouterLink>
        </div>
      </div>
    </div>
  </footer>
</template>
