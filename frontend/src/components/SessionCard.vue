<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import type { Session } from '../types'
import { loc, type Locale } from '../types'

const props = defineProps<{ session: Session; featured?: boolean }>()
const { t, locale } = useI18n()
const l = computed(() => locale.value as Locale)
const statusLabel = computed(() => t(`status.${props.session.status}` as never) || props.session.status)
const fee = computed(() => {
  const tu = props.session.tuition_usd
  const en = props.session.enrollment_fee_usd
  if (en) return `${tu} USD + ${en} USD`
  return `${tu} USD`
})
</script>

<template>
  <article
    class="group flex h-full flex-col overflow-hidden rounded-2xl border border-navy/8 bg-white p-6 shadow-soft transition duration-500 hover:-translate-y-1"
    :class="featured ? 'ring-1 ring-wine/40' : ''"
  >
    <div class="flex items-center justify-between gap-3">
      <span class="rounded-full bg-emerald-50 px-3 py-1 text-[11px] font-semibold uppercase tracking-wider text-emerald-800">
        {{ statusLabel }}
      </span>
      <span class="text-sm font-semibold text-navy">{{ fee }}</span>
    </div>
    <h3 class="mt-5 font-display text-2xl text-navy">{{ loc(session, l, 'title') }}</h3>
    <p class="mt-2 text-sm text-gold-dark">{{ loc(session, l, 'duration') }}</p>
    <p class="mt-4 flex-1 text-sm leading-relaxed text-mute">{{ loc(session, l, 'summary') }}</p>
    <RouterLink :to="{ path: '/inscription', query: { session: session.slug } }" class="btn btn-navy mt-6 w-full">
      {{ loc(session, l, 'cta') }}
    </RouterLink>
  </article>
</template>
