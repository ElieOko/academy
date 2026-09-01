<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../../lib/api'

const stats = ref<Record<string, number>>({})
onMounted(async () => {
  stats.value = (await api.get('/admin/stats')).data
})
</script>

<template>
  <div>
    <h1 class="font-display text-3xl text-navy">Tableau de bord</h1>
    <div class="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
      <article v-for="(v, k) in stats" :key="k" class="rounded-2xl bg-white p-5 shadow-soft">
        <p class="text-xs uppercase tracking-wider text-mute">{{ k }}</p>
        <p class="mt-2 font-display text-4xl text-navy">{{ v }}</p>
      </article>
    </div>
  </div>
</template>
