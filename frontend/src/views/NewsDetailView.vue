<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { api } from '../lib/api'
import type { NewsItem } from '../types'

const route = useRoute()
const { locale } = useI18n()
const item = ref<NewsItem | null>(null)

onMounted(async () => {
  const { data } = await api.get(`/news/${route.params.slug}`)
  item.value = data
})
</script>

<template>
  <main v-if="item" class="pb-24 pt-28">
    <div class="container-page max-w-3xl">
      <p class="eyebrow">{{ item.category }}</p>
      <h1 class="mt-4 font-display text-4xl text-navy md:text-5xl">
        {{ locale === 'en' ? item.title_en : item.title_fr }}
      </h1>
      <img v-if="item.image_url" :src="item.image_url" alt="" class="mt-8 h-72 w-full rounded-2xl object-cover" />
      <div class="mt-8 whitespace-pre-line text-base leading-relaxed text-ink/90">
        {{ locale === 'en' ? item.content_en : item.content_fr }}
      </div>
    </div>
  </main>
</template>
