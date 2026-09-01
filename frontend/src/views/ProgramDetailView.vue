<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { api } from '../lib/api'
import { loc, type Locale, type Program } from '../types'
import { programCover } from '../lib/covers'

const route = useRoute()
const { t, locale } = useI18n()
const l = computed(() => locale.value as Locale)
const program = ref<Program | null>(null)
const error = ref('')

onMounted(async () => {
  try {
    const { data } = await api.get(`/programs/${route.params.slug}`)
    program.value = data
  } catch {
    error.value = '404'
  }
})
</script>

<template>
  <main class="pb-24 pt-28">
    <div v-if="error" class="container-page">Formation introuvable.</div>
    <div v-else-if="program">
      <section class="relative h-[42vh] min-h-[280px] overflow-hidden">
        <img :src="programCover(program.slug, program.image_url)" alt="" class="absolute inset-0 h-full w-full object-cover" />
        <div class="absolute inset-0 bg-navy/70" />
        <div class="container-page relative flex h-full flex-col justify-end pb-10 text-white">
          <p class="eyebrow text-gold">{{ program.code }}</p>
          <h1 class="mt-3 font-display text-4xl md:text-6xl">{{ loc(program, l, 'title') }}</h1>
          <p class="mt-3 max-w-2xl text-white/80">{{ loc(program, l, 'tagline') }}</p>
        </div>
      </section>
      <div class="container-page grid gap-12 py-14 lg:grid-cols-[1.4fr_0.8fr]">
        <div>
          <p class="text-lg leading-relaxed text-navy">{{ loc(program, l, 'description') }}</p>
          <h2 class="mt-10 font-display text-2xl">{{ t('programs.objectives') }}</h2>
          <ul class="mt-4 space-y-2 text-sm text-mute">
            <li v-for="o in program.objectives" :key="o.fr" class="flex gap-2">
              <span class="mt-1 h-1.5 w-1.5 shrink-0 rounded-full bg-gold" />
              {{ l === 'en' ? o.en : o.fr }}
            </li>
          </ul>
          <h2 class="mt-10 font-display text-2xl">{{ t('programs.audience') }}</h2>
          <p class="mt-3 text-sm leading-relaxed text-mute">{{ loc(program, l, 'audience') }}</p>
          <h2 class="mt-10 font-display text-2xl">{{ t('programs.modules') }}</h2>
          <ol class="mt-4 grid gap-3 sm:grid-cols-2">
            <li v-for="(m, i) in program.modules" :key="m.fr" class="rounded-xl bg-white p-4 shadow-soft">
              <span class="text-xs text-gold-dark">0{{ i + 1 }}</span>
              <p class="mt-1 text-sm text-navy">{{ l === 'en' ? m.en : m.fr }}</p>
            </li>
          </ol>
          <h2 class="mt-10 font-display text-2xl">{{ t('programs.prereq') }}</h2>
          <p class="mt-3 text-sm text-mute">{{ loc(program, l, 'prerequisites') }}</p>
        </div>
        <aside class="h-fit rounded-2xl bg-white p-6 shadow-soft">
          <h3 class="font-display text-xl">{{ t('programs.next') }}</h3>
          <div v-if="program.sessions?.length" class="mt-4 space-y-4">
            <article v-for="s in program.sessions" :key="s.id" class="border-t border-navy/8 pt-4">
              <p class="font-medium">{{ loc(s, l, 'title') }}</p>
              <p class="text-xs text-mute">{{ loc(s, l, 'duration') }}</p>
              <p class="mt-1 text-sm">{{ s.tuition_usd }} USD</p>
              <RouterLink :to="{ path: '/inscription', query: { session: s.slug } }" class="btn btn-navy mt-3 w-full py-2 text-xs">
                {{ loc(s, l, 'cta') }}
              </RouterLink>
            </article>
          </div>
          <p v-else class="mt-3 text-sm text-mute">{{ t('programs.none') }}</p>
          <RouterLink to="/inscription" class="btn btn-wine mt-6 w-full">{{ t('cta.enroll') }}</RouterLink>
        </aside>
      </div>
    </div>
  </main>
</template>
