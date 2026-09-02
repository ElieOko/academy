<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { MessageCircle } from '@lucide/vue'
import SectionTitle from '../components/SectionTitle.vue'
import SessionCard from '../components/SessionCard.vue'
import ProgramCard from '../components/ProgramCard.vue'
import { useCatalog } from '../stores'

const { t, locale } = useI18n()
const catalog = useCatalog()
const highlighted = computed(() => {
  const order = ['english-level-1', 'english-level-2', 'speaking-lab']
  return [...catalog.highlighted].sort((a, b) => {
    const ia = order.indexOf(a.slug)
    const ib = order.indexOf(b.slug)
    return (ia === -1 ? 99 : ia) - (ib === -1 ? 99 : ib)
  })
})
const whatsapp = computed(() => {
  const n = catalog.contact.whatsapp || '243810000243'
  return `https://wa.me/${n}`
})

const slides = ['/images/back-01.jpg', '/images/back-02.jpg', '/images/back-03.jpg']
const gallery = ['/images/gallery-01.jpg', '/images/gallery-02.jpg', '/images/gallery-03.jpg']
const slide = ref(0)
const mx = ref(0)
const my = ref(0)
let timer = 0

function onMove(e: MouseEvent) {
  mx.value = (e.clientX / window.innerWidth - 0.5) * 28
  my.value = (e.clientY / window.innerHeight - 0.5) * 18
}

onMounted(() => {
  timer = window.setInterval(() => {
    slide.value = (slide.value + 1) % slides.length
  }, 6500)
  window.addEventListener('mousemove', onMove, { passive: true })
})

onUnmounted(() => {
  window.clearInterval(timer)
  window.removeEventListener('mousemove', onMove)
})
</script>

<template>
  <main>
    <section class="relative min-h-[100svh] overflow-hidden">
      <div
        class="absolute -inset-10 will-change-transform"
        :style="{ transform: `translate3d(${mx}px, ${my}px, 0)` }"
      >
        <img
          v-for="(src, i) in slides"
          :key="src"
          :src="src"
          alt=""
          class="absolute inset-0 h-full w-full object-cover transition-opacity duration-[1400ms] ease-in-out"
          :class="i === slide ? 'opacity-100 kenburns' : 'opacity-0'"
        />
      </div>
      <div class="absolute inset-0 bg-gradient-to-r from-navy/90 via-navy/72 to-navy/35" />
      <div class="container-page relative flex min-h-[100svh] flex-col justify-end pb-20 pt-32 md:justify-center md:pb-0">
        <p v-reveal class="eyebrow text-gold">{{ t('hero.kicker') }} · {{ t('parent') }}</p>
        <h1 v-reveal="80" class="mt-5 max-w-3xl font-display text-5xl leading-[1.05] text-white md:text-7xl">
          {{ t('slogan') }}
        </h1>
        <p v-reveal="160" class="mt-6 max-w-xl text-lg text-white/80">{{ t('promise') }}</p>
        <p v-reveal="200" class="mt-2 max-w-xl text-white/65">{{ t('promiseLong') }}</p>
        <div v-reveal="260" class="mt-9 flex flex-col gap-3 sm:flex-row">
          <RouterLink to="/formations" class="btn btn-wine">{{ t('cta.discover') }}</RouterLink>
          <RouterLink to="/inscription" class="btn bg-white text-navy hover:bg-gold-light">{{ t('cta.enroll') }}</RouterLink>
          <a :href="whatsapp" target="_blank" class="btn btn-ghost">
            <MessageCircle :size="16" /> {{ t('cta.advisor') }}
          </a>
        </div>
        <div class="mt-10 flex items-center gap-2">
          <button
            v-for="(_, i) in slides"
            :key="i"
            type="button"
            class="h-1.5 rounded-full transition-all"
            :class="i === slide ? 'w-8 bg-wine' : 'w-3 bg-white/40'"
            :aria-label="`Slide ${i + 1}`"
            @click="slide = i"
          />
        </div>
      </div>
    </section>

    <section class="bg-cream py-20">
      <div class="container-page">
        <SectionTitle :title="t('sections.openSessions')" :lead="t('englishBanner')" />
        <div class="mt-10 grid gap-6 md:grid-cols-3">
          <div v-for="(s, i) in highlighted" :key="s.id" v-reveal="i * 80">
            <SessionCard :session="s" featured />
          </div>
          <p v-if="!highlighted.length" class="text-mute">{{ t('empty.sessions') }}</p>
        </div>
      </div>
    </section>

    <section class="bg-white py-20">
      <div class="container-page">
        <SectionTitle :title="t('sections.programs')" :lead="t('sections.programsLead')" />
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div v-for="(p, i) in catalog.programs" :key="p.id" v-reveal="i * 60">
            <ProgramCard :program="p" />
          </div>
          <p v-if="!catalog.programs.length" class="col-span-full text-mute">{{ t('empty.programs') }}</p>
        </div>
      </div>
    </section>

    <section class="bg-navy py-20 text-white">
      <div class="container-page">
        <SectionTitle light kicker="ACAD’EMY" :title="t('sections.advantages')" />
        <div class="mt-12 grid gap-8 md:grid-cols-4">
          <article v-for="n in 4" :key="n" v-reveal="n * 70" class="border-t border-gold/40 pt-6">
            <p class="font-display text-2xl text-gold">0{{ n }}</p>
            <h3 class="mt-3 text-lg">{{ t(`advantages.a${n}t`) }}</h3>
            <p class="mt-2 text-sm leading-relaxed text-white/65">{{ t(`advantages.a${n}d`) }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="bg-cream py-20">
      <div class="container-page grid items-center gap-12 lg:grid-cols-2">
        <div>
          <SectionTitle :title="t('sections.method')" :lead="t('sections.methodLead')" />
          <ol class="mt-10 space-y-6">
            <li v-for="n in 4" :key="n" v-reveal="n * 60" class="flex gap-4">
              <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-navy font-display text-gold">{{ n }}</span>
              <div>
                <h3 class="font-medium text-navy">{{ t(`method.s${n}t`) }}</h3>
                <p class="mt-1 text-sm text-mute">{{ t(`method.s${n}d`) }}</p>
              </div>
            </li>
          </ol>
        </div>
        <div v-reveal class="grid grid-cols-2 gap-3">
          <img :src="gallery[0]" alt="" class="h-72 w-full rounded-2xl object-cover" />
          <img :src="gallery[1]" alt="" class="mt-10 h-72 w-full rounded-2xl object-cover" />
        </div>
      </div>
    </section>

    <section class="bg-white py-20">
      <div class="container-page">
        <SectionTitle :title="t('sections.upcoming')" />
        <div v-if="catalog.sessions.length" class="mt-8 overflow-hidden rounded-2xl border border-navy/8">
          <div
            v-for="s in catalog.sessions"
            :key="s.id"
            class="flex flex-col gap-3 border-b border-navy/8 px-5 py-5 last:border-0 md:flex-row md:items-center md:justify-between"
          >
            <div>
              <p class="font-medium text-navy">{{ locale === 'en' ? s.title_en : s.title_fr }}</p>
              <p class="text-sm text-mute">{{ locale === 'en' ? s.duration_en : s.duration_fr }}</p>
            </div>
            <div class="flex flex-wrap items-center gap-3">
              <span class="text-sm font-semibold">{{ s.tuition_usd }} USD</span>
              <RouterLink :to="{ path: '/inscription', query: { session: s.slug } }" class="btn btn-navy">
                {{ locale === 'en' ? s.cta_en : s.cta_fr }}
              </RouterLink>
            </div>
          </div>
        </div>
        <p v-else class="mt-8 text-mute">{{ t('empty.sessions') }}</p>
      </div>
    </section>

    <section v-if="catalog.testimonials.length" class="bg-cream py-20">
      <div class="container-page">
        <SectionTitle :title="t('sections.voices')" />
        <div class="mt-10 grid gap-6 md:grid-cols-3">
          <blockquote
            v-for="(item, i) in catalog.testimonials"
            :key="item.id"
            v-reveal="i * 80"
            class="rounded-2xl bg-white p-6 shadow-soft"
          >
            <p class="text-sm leading-relaxed text-ink">“{{ locale === 'en' ? item.quote_en : item.quote_fr }}”</p>
            <footer class="mt-5">
              <p class="font-medium text-navy">{{ item.name }}</p>
              <p class="text-xs text-mute">{{ locale === 'en' ? item.role_en : item.role_fr }}</p>
            </footer>
          </blockquote>
        </div>
      </div>
    </section>

    <section class="relative overflow-hidden py-24">
      <img :src="gallery[2]" alt="" class="absolute inset-0 h-full w-full object-cover" />
      <div class="absolute inset-0 bg-navy/85" />
      <div class="container-page relative text-center text-white">
        <p class="eyebrow text-gold">ACAD’EMY</p>
        <h2 class="mt-4 font-display text-4xl md:text-5xl">{{ t('sections.final') }}</h2>
        <p class="mx-auto mt-4 max-w-xl text-white/70">{{ t('sections.finalLead') }}</p>
        <div class="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <RouterLink to="/inscription" class="btn btn-wine">{{ t('cta.enroll') }}</RouterLink>
          <a :href="whatsapp" target="_blank" class="btn btn-ghost">{{ t('cta.advisor') }}</a>
        </div>
      </div>
    </section>
  </main>
</template>
