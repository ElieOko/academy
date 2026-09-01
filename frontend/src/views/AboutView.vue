<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'

const { t } = useI18n()
const keys = ['excellence', 'pratique', 'innovation', 'rigueur', 'ethique', 'impact'] as const
const photos = [
  '/images/gallery-01.jpg',
  '/images/gallery-02.jpg',
  '/images/gallery-03.jpg',
  '/images/back-01.jpg',
  '/images/back-02.jpg',
  '/images/back-03.jpg',
]
</script>

<template>
  <main class="pt-28">
    <section class="container-page pb-16">
      <SectionTitle :title="t('about.title')" :lead="t('about.lead')" />
      <div class="mt-12 grid gap-8 md:grid-cols-2">
        <article v-reveal class="rounded-2xl bg-white p-8 shadow-soft">
          <p class="eyebrow">{{ t('about.missionT') }}</p>
          <p class="mt-4 text-lg leading-relaxed text-navy">{{ t('about.mission') }}</p>
        </article>
        <article v-reveal="80" class="relative overflow-hidden rounded-2xl bg-navy p-8 text-white shadow-soft">
          <img src="/images/back-03.jpg" alt="" class="absolute inset-0 h-full w-full object-cover opacity-25" />
          <div class="relative">
            <p class="eyebrow text-gold">{{ t('about.visionT') }}</p>
            <p class="mt-4 text-lg leading-relaxed text-white/85">{{ t('about.vision') }}</p>
          </div>
        </article>
      </div>
    </section>

    <section class="bg-white py-20">
      <div class="container-page">
        <SectionTitle :title="t('about.valuesT')" />
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <article v-for="(k, i) in keys" :key="k" v-reveal="i * 50" class="border-t border-wine pt-5">
            <h3 class="font-display text-2xl text-navy">{{ t(`about.values.${k}.t`) }}</h3>
            <p class="mt-2 text-sm text-mute">{{ t(`about.values.${k}.d`) }}</p>
          </article>
        </div>
      </div>
    </section>

    <section class="container-page py-20">
      <SectionTitle :title="t('about.approachT')" :lead="t('about.approach')" />
    </section>

    <section class="bg-cream pb-24">
      <div class="container-page">
        <SectionTitle :title="t('about.galleryT')" />
        <div class="mt-10 grid gap-4 md:grid-cols-3">
          <img
            v-for="(src, i) in photos"
            :key="src"
            v-reveal="i * 70"
            :src="src"
            alt=""
            class="h-64 w-full rounded-2xl object-cover md:h-72"
            :class="i === 0 || i === 5 ? 'md:col-span-2' : ''"
          />
        </div>
      </div>
    </section>
  </main>
</template>
