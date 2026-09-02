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
  { to: '/contact', label: t('nav.contact') },
])
</script>

<template>
  <footer class="mt-auto bg-navy text-white">
    <div class="container-page grid gap-10 py-16 md:grid-cols-4">
      <div class="md:col-span-2">
        <div class="flex items-center gap-3">
          <span class="flex h-12 w-12 items-center justify-center overflow-hidden rounded-xl bg-white">
            <img src="/images/academy-mark.jpg" alt="" class="h-20 w-20 object-contain transition-transform scale-150" />
          </span>
          <p class="font-display text-3xl">Acad’Emy</p>
        </div>
        <p class="mt-4 max-w-md text-sm leading-relaxed text-white/70">
          {{ t('promiseLong') }}
        </p>
        <div class="mt-6 flex items-center gap-3">
          <span class="rounded-md bg-white px-2 py-1">
            <img src="/images/lawapp-logo.jpg" alt="LawApp50 Group" class="h-10 w-auto object-contain" />
          </span>
          <p class="text-xs uppercase tracking-[0.18em] text-white/40">{{ t('parent') }}</p>
        </div>
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
