<script setup lang="ts">
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
</script>

<template>
  <main class="container-page max-w-2xl pb-24 pt-28">
    <h1 class="font-display text-4xl text-navy">{{ t('privacy.title') }}</h1>
    <p class="mt-6 leading-relaxed text-mute">{{ t('privacy.body') }}</p>
  </main>
</template>
