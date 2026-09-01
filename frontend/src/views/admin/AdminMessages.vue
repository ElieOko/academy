<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../../lib/api'

const rows = ref<Record<string, unknown>[]>([])
onMounted(async () => {
  rows.value = (await api.get('/admin/messages')).data
})
</script>

<template>
  <div>
    <h1 class="font-display text-3xl text-navy">Messages</h1>
    <div class="mt-6 space-y-4">
      <article v-for="r in rows" :key="String(r.id)" class="rounded-2xl bg-white p-5 shadow-soft">
        <p class="font-medium">{{ r.name }} · {{ r.email }}</p>
        <p class="text-xs text-mute">{{ r.phone }} · {{ r.created_at }}</p>
        <p class="mt-3 text-sm">{{ r.message }}</p>
      </article>
      <p v-if="!rows.length" class="text-mute">Aucun message.</p>
    </div>
  </div>
</template>
