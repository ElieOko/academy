<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../lib/api'

const programs = ref<{ id: string; title_fr: string }[]>([])
const rows = ref<Record<string, unknown>[]>([])
const editing = ref<Record<string, unknown> | null>(null)
const form = reactive({
  program_id: '',
  slug: '',
  title_fr: '',
  title_en: '',
  summary_fr: '',
  summary_en: '',
  start_date: '',
  end_date: '',
  duration_fr: '',
  duration_en: '',
  status: 'open',
  tuition_usd: 0,
  enrollment_fee_usd: 0,
  format: 'in_person',
  cta_fr: "S'inscrire",
  cta_en: 'Enroll',
  is_highlighted: false,
  max_seats: null as number | null,
})

async function refresh() {
  programs.value = (await api.get('/admin/programs')).data
  rows.value = (await api.get('/admin/sessions')).data
}
onMounted(refresh)

function create() {
  fill({
    program_id: '',
    slug: '',
    title_fr: '',
    title_en: '',
    summary_fr: '',
    summary_en: '',
    start_date: '',
    end_date: '',
    duration_fr: '',
    duration_en: '',
    status: 'open',
    tuition_usd: 0,
    enrollment_fee_usd: 0,
    format: 'in_person',
    cta_fr: "S'inscrire",
    cta_en: 'Enroll',
    is_highlighted: false,
    max_seats: null,
  })
}

function fill(r: Record<string, unknown>) {
  editing.value = r
  Object.assign(form, {
    program_id: r.program_id,
    slug: r.slug,
    title_fr: r.title_fr,
    title_en: r.title_en,
    summary_fr: r.summary_fr,
    summary_en: r.summary_en,
    start_date: r.start_date || '',
    end_date: r.end_date || '',
    duration_fr: r.duration_fr,
    duration_en: r.duration_en,
    status: r.status,
    tuition_usd: r.tuition_usd,
    enrollment_fee_usd: r.enrollment_fee_usd,
    format: r.format,
    cta_fr: r.cta_fr,
    cta_en: r.cta_en,
    is_highlighted: r.is_highlighted,
    max_seats: r.max_seats,
  })
}

async function save() {
  const body = {
    ...form,
    start_date: form.start_date || null,
    end_date: form.end_date || null,
    tuition_usd: Number(form.tuition_usd),
    enrollment_fee_usd: Number(form.enrollment_fee_usd),
  }
  if (editing.value?.id) await api.put(`/admin/sessions/${editing.value.id}`, body)
  else await api.post('/admin/sessions', body)
  editing.value = null
  await refresh()
}

async function remove(id: string) {
  if (!confirm('Supprimer cette session ?')) return
  await api.delete(`/admin/sessions/${id}`)
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between">
      <h1 class="font-display text-3xl text-navy">Sessions</h1>
      <button class="btn btn-navy py-2" @click="create">Nouvelle</button>
    </div>
    <form v-if="editing" class="mt-6 grid gap-3 rounded-2xl bg-white p-6 shadow-soft md:grid-cols-2" @submit.prevent="save">
      <select v-model="form.program_id" required>
        <option value="" disabled>Formation</option>
        <option v-for="p in programs" :key="p.id" :value="p.id">{{ p.title_fr }}</option>
      </select>
      <input v-model="form.slug" placeholder="slug" required />
      <input v-model="form.title_fr" placeholder="Titre FR" required />
      <input v-model="form.title_en" placeholder="Title EN" required />
      <textarea v-model="form.summary_fr" rows="3" placeholder="Résumé FR" />
      <textarea v-model="form.summary_en" rows="3" placeholder="Summary EN" />
      <input v-model="form.start_date" type="date" />
      <input v-model="form.end_date" type="date" />
      <input v-model="form.duration_fr" placeholder="Durée FR" />
      <input v-model="form.duration_en" placeholder="Duration EN" />
      <select v-model="form.status">
        <option value="open">open</option>
        <option value="upcoming">upcoming</option>
        <option value="closed">closed</option>
        <option value="full">full</option>
      </select>
      <select v-model="form.format">
        <option value="in_person">présentiel</option>
        <option value="online">en ligne</option>
        <option value="hybrid">hybride</option>
      </select>
      <input v-model="form.tuition_usd" type="number" step="0.01" placeholder="Frais formation" />
      <input v-model="form.enrollment_fee_usd" type="number" step="0.01" placeholder="Frais inscription" />
      <input v-model="form.cta_fr" placeholder="Bouton FR" />
      <input v-model="form.cta_en" placeholder="Button EN" />
      <label class="flex items-center gap-2 text-sm md:col-span-2">
        <input v-model="form.is_highlighted" type="checkbox" class="w-auto" /> Mettre en avant (accueil)
      </label>
      <div class="flex gap-2 md:col-span-2">
        <button class="btn btn-gold">Enregistrer</button>
        <button type="button" class="btn btn-outline" @click="editing = null">Annuler</button>
      </div>
    </form>
    <div class="mt-6 overflow-x-auto rounded-2xl bg-white shadow-soft">
      <table class="w-full text-left text-sm">
        <thead class="text-xs uppercase text-mute">
          <tr><th class="p-4">Session</th><th>Dates</th><th>Statut</th><th>Frais</th><th></th></tr>
        </thead>
        <tbody>
          <tr v-for="r in rows" :key="String(r.id)" class="border-t border-navy/5">
            <td class="p-4">{{ r.title_fr }}</td>
            <td>{{ r.start_date }}</td>
            <td>{{ r.status }}</td>
            <td>{{ r.tuition_usd }} USD</td>
            <td class="p-4 text-right">
              <button class="mr-3" @click="fill(r)">Modifier</button>
              <button class="text-red-600" @click="remove(String(r.id))">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
