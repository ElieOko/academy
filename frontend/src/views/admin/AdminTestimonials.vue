<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../lib/api'

const rows = ref<Record<string, unknown>[]>([])
const editing = ref<Record<string, unknown> | null>(null)
const form = reactive({
  name: '',
  role_fr: '',
  role_en: '',
  quote_fr: '',
  quote_en: '',
  photo_url: '',
  is_published: true,
  sort_order: 0,
})

async function refresh() {
  rows.value = (await api.get('/admin/testimonials')).data
}
onMounted(refresh)

function fill(r: Record<string, unknown> = {}) {
  editing.value = r
  Object.assign(form, {
    name: r.name || '',
    role_fr: r.role_fr || '',
    role_en: r.role_en || '',
    quote_fr: r.quote_fr || '',
    quote_en: r.quote_en || '',
    photo_url: r.photo_url || '',
    is_published: r.is_published !== false,
    sort_order: r.sort_order || 0,
  })
}

async function save() {
  const body = { ...form, sort_order: Number(form.sort_order) }
  if (editing.value?.id) await api.put(`/admin/testimonials/${editing.value.id}`, body)
  else await api.post('/admin/testimonials', body)
  editing.value = null
  await refresh()
}

async function remove(id: string) {
  if (!confirm('Supprimer ?')) return
  await api.delete(`/admin/testimonials/${id}`)
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between">
      <h1 class="font-display text-3xl text-navy">Témoignages</h1>
      <button class="btn btn-navy py-2" @click="fill()">Nouveau</button>
    </div>
    <form v-if="editing" class="mt-6 grid gap-3 rounded-2xl bg-white p-6 shadow-soft md:grid-cols-2" @submit.prevent="save">
      <input v-model="form.name" placeholder="Nom" required />
      <input v-model="form.sort_order" type="number" placeholder="Ordre" />
      <input v-model="form.role_fr" placeholder="Rôle FR" />
      <input v-model="form.role_en" placeholder="Role EN" />
      <textarea v-model="form.quote_fr" rows="3" placeholder="Citation FR" />
      <textarea v-model="form.quote_en" rows="3" placeholder="Quote EN" />
      <input v-model="form.photo_url" placeholder="Photo URL" class="md:col-span-2" />
      <label class="flex items-center gap-2 text-sm"><input v-model="form.is_published" type="checkbox" class="w-auto" /> Publié</label>
      <div class="flex gap-2 md:col-span-2">
        <button class="btn btn-wine">Enregistrer</button>
        <button type="button" class="btn btn-outline" @click="editing = null">Annuler</button>
      </div>
    </form>
    <div class="mt-6 space-y-3">
      <article v-for="r in rows" :key="String(r.id)" class="rounded-2xl bg-white p-4 shadow-soft">
        <p class="font-medium">{{ r.name }} — {{ r.role_fr }}</p>
        <p class="mt-1 text-sm text-mute">{{ r.quote_fr }}</p>
        <div class="mt-3">
          <button class="mr-3" @click="fill(r)">Modifier</button>
          <button class="text-red-600" @click="remove(String(r.id))">Supprimer</button>
        </div>
      </article>
    </div>
  </div>
</template>
