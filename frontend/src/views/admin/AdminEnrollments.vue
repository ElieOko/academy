<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../../lib/api'

const rows = ref<Record<string, unknown>[]>([])
async function refresh() {
  rows.value = (await api.get('/admin/enrollments')).data
}
onMounted(refresh)

async function setStatus(id: string, status: string) {
  await api.patch(`/admin/enrollments/${id}`, { status, notes: '' })
  await refresh()
}
</script>

<template>
  <div>
    <h1 class="font-display text-3xl text-navy">Inscriptions</h1>
    <div class="mt-6 overflow-x-auto rounded-2xl bg-white shadow-soft">
      <table class="w-full min-w-[800px] text-left text-sm">
        <thead class="text-xs uppercase text-mute">
          <tr>
            <th class="p-4">Nom</th>
            <th>WhatsApp</th>
            <th>E-mail</th>
            <th>Formation</th>
            <th>Session</th>
            <th>Format</th>
            <th>Statut</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in rows" :key="String(r.id)" class="border-t border-navy/5 align-top">
            <td class="p-4">
              <p class="font-medium">{{ r.full_name }}</p>
              <p class="text-xs text-mute">{{ r.objective }}</p>
            </td>
            <td>{{ r.whatsapp }}</td>
            <td>{{ r.email }}</td>
            <td>{{ (r.program as { title_fr?: string } | null)?.title_fr }}</td>
            <td>{{ (r.session as { title_fr?: string } | null)?.title_fr }}</td>
            <td>{{ r.format_preference }}</td>
            <td class="p-4">
              <select :value="r.status" class="w-36" @change="setStatus(String(r.id), ($event.target as HTMLSelectElement).value)">
                <option value="pending">pending</option>
                <option value="contacted">contacted</option>
                <option value="confirmed">confirmed</option>
                <option value="cancelled">cancelled</option>
              </select>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
