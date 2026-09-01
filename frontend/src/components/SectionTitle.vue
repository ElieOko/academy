<script setup lang="ts">
defineProps<{ kicker?: string; title: string; lead?: string; light?: boolean }>()
</script>

<template>
  <div class="max-w-2xl">
    <p v-if="kicker" class="eyebrow" :class="light ? 'text-gold' : ''">{{ kicker }}</p>
    <div class="gold-rule mt-3" :class="light ? 'bg-gold' : ''" />
    <h2 class="mt-4 font-display text-3xl md:text-4xl" :class="light ? 'text-white' : 'text-navy'">{{ title }}</h2>
    <p v-if="lead" class="mt-3" :class="light ? 'text-white/70' : 'text-mute'">{{ lead }}</p>
  </div>
</template>
