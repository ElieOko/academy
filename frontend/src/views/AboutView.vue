<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'

const { t } = useI18n()
const keys = ['excellence', 'pratique', 'innovation', 'rigueur', 'ethique', 'impact'] as const
const photos = [
  'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1522202176988-66273c2fd55f?auto=format&fit=crop&w=1200&q=80',
  'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80',
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
        <article v-reveal="80" class="rounded-2xl bg-navy p-8 text-white shadow-soft">
          <p class="eyebrow text-gold">{{ t('about.visionT') }}</p>
          <p class="mt-4 text-lg leading-relaxed text-white/85">{{ t('about.vision') }}</p>
        </article>
      </div>
    </section>

    <section class="bg-white py-20">
      <div class="container-page">
        <SectionTitle :title="t('about.valuesT')" />
        <div class="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <article v-for="(k, i) in keys" :key="k" v-reveal="i * 50" class="border-t border-gold pt-5">
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
        <div class="mt-10 grid gap-4 md:grid-cols-2">
          <img v-for="(src, i) in photos" :key="src" v-reveal="i * 70" :src="src" alt="" class="h-64 w-full rounded-2xl object-cover md:h-80" />
        </div>
        <p class="mt-4 text-xs text-mute">Photos d’ambiance — à remplacer par les visuels autorisés du centre.</p>
      </div>
    </section>
  </main>
</template>
