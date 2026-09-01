<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'
import SessionCard from '../components/SessionCard.vue'
import { useCatalog } from '../stores'

const { t } = useI18n()
const catalog = useCatalog()
</script>

<template>
  <main class="container-page pb-24 pt-28">
    <SectionTitle :title="t('calendar.title')" :lead="t('calendar.lead')" />
    <div class="mt-12 grid gap-6 md:grid-cols-3">
      <SessionCard v-for="s in catalog.sessions" :key="s.id" :session="s" :featured="s.is_highlighted" />
    </div>
  </main>
</template>
