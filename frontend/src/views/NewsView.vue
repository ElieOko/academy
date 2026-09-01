<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'
import { useCatalog } from '../stores'

const { t, locale } = useI18n()
const catalog = useCatalog()
</script>

<template>
  <main class="container-page pb-24 pt-28">
    <SectionTitle :title="t('news.title')" :lead="t('news.lead')" />
    <div v-if="!catalog.news.length" class="mt-10 flex flex-1 items-start text-mute">{{ t('news.empty') }}</div>
    <div class="mt-12 grid gap-6 md:grid-cols-3">
      <RouterLink
        v-for="(n, i) in catalog.news"
        :key="n.id"
        v-reveal="i * 60"
        :to="`/actualites/${n.slug}`"
        class="overflow-hidden rounded-2xl bg-white shadow-soft transition hover:-translate-y-1"
      >
        <img :src="n.image_url" alt="" class="h-44 w-full object-cover" />
        <div class="p-5">
          <p class="text-[11px] uppercase tracking-wider text-gold-dark">{{ n.category }}</p>
          <h3 class="mt-2 font-display text-xl text-navy">{{ locale === 'en' ? n.title_en : n.title_fr }}</h3>
          <p class="mt-2 line-clamp-3 text-sm text-mute">{{ locale === 'en' ? n.excerpt_en : n.excerpt_fr }}</p>
        </div>
      </RouterLink>
    </div>
  </main>
</template>
