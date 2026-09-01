<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { ArrowUpRight } from '@lucide/vue'
import type { Program } from '../types'
import { loc, type Locale } from '../types'

const props = defineProps<{ program: Program }>()
const { t, locale } = useI18n()
const l = computed(() => locale.value as Locale)
</script>

<template>
  <RouterLink
    :to="`/formations/${program.slug}`"
    class="group overflow-hidden rounded-2xl bg-white shadow-soft transition duration-500 hover:-translate-y-1"
  >
    <div class="relative h-48 overflow-hidden">
      <img :src="program.image_url" :alt="loc(program, l, 'title')" class="h-full w-full object-cover transition duration-700 group-hover:scale-105" />
      <span class="absolute left-4 top-4 rounded-full bg-navy/85 px-3 py-1 text-[11px] font-semibold tracking-wider text-gold">
        {{ program.code }}
      </span>
    </div>
    <div class="p-6">
      <h3 class="font-display text-2xl text-navy">{{ loc(program, l, 'title') }}</h3>
      <p class="mt-2 text-sm text-gold-dark">{{ loc(program, l, 'tagline') }}</p>
      <p class="mt-3 line-clamp-3 text-sm leading-relaxed text-mute">{{ loc(program, l, 'description') }}</p>
      <span class="mt-5 inline-flex items-center gap-1 text-sm font-medium text-navy">
        {{ t('programs.detail') }} <ArrowUpRight :size="16" />
      </span>
    </div>
  </RouterLink>
</template>
