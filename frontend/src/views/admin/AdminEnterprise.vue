<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../../lib/api'

const rows = ref<Record<string, unknown>[]>([])
async function refresh() {
  rows.value = (await api.get('/admin/enterprise')).data
}
onMounted(refresh)

async function setStatus(id: string, status: string) {
  await api.patch(`/admin/enterprise/${id}`, { status })
  await refresh()
}
</script>

<template>
  <div>
    <h1 class="font-display text-3xl text-navy">Demandes entreprises</h1>
    <div class="mt-6 space-y-4">
      <article v-for="r in rows" :key="String(r.id)" class="rounded-2xl bg-white p-5 shadow-soft">
        <div class="flex flex-wrap items-start justify-between gap-3">
          <div>
            <p class="font-medium">{{ r.company }} — {{ r.contact_name }}</p>
            <p class="text-sm text-mute">{{ r.email }} · {{ r.phone }}</p>
            <p class="mt-2 text-sm">{{ r.topics }}</p>
            <p class="mt-1 text-sm text-mute">{{ r.message }}</p>
          </div>
          <select :value="r.status" class="w-40" @change="setStatus(String(r.id), ($event.target as HTMLSelectElement).value)">
            <option value="new">new</option>
            <option value="contacted">contacted</option>
            <option value="done">done</option>
          </select>
        </div>
      </article>
      <p v-if="!rows.length" class="text-mute">Aucune demande pour le moment.</p>
    </div>
  </div>
</template>
