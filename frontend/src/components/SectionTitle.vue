<script setup lang="ts">
defineProps<{ kicker?: string; title: string; lead?: string }>()
</script>

<template>
  <div class="max-w-2xl">
    <p v-if="kicker" class="eyebrow">{{ kicker }}</p>
    <div class="gold-rule mt-3" />
    <h2 class="mt-4 font-display text-3xl text-navy md:text-4xl">{{ title }}</h2>
    <p v-if="lead" class="mt-3 text-mute">{{ lead }}</p>
  </div>
</template>
