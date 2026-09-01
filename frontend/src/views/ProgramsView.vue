<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'
import ProgramCard from '../components/ProgramCard.vue'
import { useCatalog } from '../stores'

const { t } = useI18n()
const catalog = useCatalog()
</script>

<template>
  <main class="container-page pb-24 pt-28">
    <SectionTitle :title="t('programs.title')" :lead="t('programs.lead')" />
    <div class="mt-12 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
      <div v-for="(p, i) in catalog.programs" :key="p.id" v-reveal="i * 50">
        <ProgramCard :program="p" />
      </div>
      <p v-if="!catalog.programs.length" class="text-mute">{{ t('empty.programs') }}</p>
    </div>
  </main>
</template>
