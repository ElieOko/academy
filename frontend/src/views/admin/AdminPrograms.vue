<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../lib/api'

type Program = Record<string, unknown> & { id?: string }

const rows = ref<Program[]>([])
const editing = ref<Program | null>(null)
const form = reactive(empty())

function empty(): Program {
  return {
    slug: '',
    code: '',
    title_fr: '',
    title_en: '',
    tagline_fr: '',
    tagline_en: '',
    description_fr: '',
    description_en: '',
    audience_fr: '',
    audience_en: '',
    prerequisites_fr: '',
    prerequisites_en: '',
    image_url: '',
    category: '',
    is_featured: true,
    is_published: true,
    sort_order: 0,
    obj_fr: '',
    obj_en: '',
    mod_fr: '',
    mod_en: '',
  }
}

function zip(a: string, b: string) {
  const aa = a.split('\n').map((s) => s.trim()).filter(Boolean)
  const bb = b.split('\n').map((s) => s.trim())
  return aa.map((fr, i) => ({ fr, en: bb[i] || fr }))
}

function loadForm(p: Program) {
  Object.assign(form, empty(), p)
  const obj = (p.objectives as { fr: string; en: string }[]) || []
  const mod = (p.modules as { fr: string; en: string }[]) || []
  form.obj_fr = obj.map((x) => x.fr).join('\n')
  form.obj_en = obj.map((x) => x.en).join('\n')
  form.mod_fr = mod.map((x) => x.fr).join('\n')
  form.mod_en = mod.map((x) => x.en).join('\n')
}

async function refresh() {
  rows.value = (await api.get('/admin/programs')).data
}

onMounted(refresh)

function payload() {
  const { obj_fr, obj_en, mod_fr, mod_en, id, created_at, updated_at, ...rest } = form as Program & {
    obj_fr: string
    obj_en: string
    mod_fr: string
    mod_en: string
  }
  return {
    ...rest,
    sort_order: Number(rest.sort_order || 0),
    objectives: zip(String(obj_fr), String(obj_en)),
    modules: zip(String(mod_fr), String(mod_en)),
  }
}

async function save() {
  const body = payload()
  if (editing.value?.id) await api.put(`/admin/programs/${editing.value.id}`, body)
  else await api.post('/admin/programs', body)
  editing.value = null
  Object.assign(form, empty())
  await refresh()
}

async function remove(id: string) {
  if (!confirm('Supprimer cette formation ?')) return
  await api.delete(`/admin/programs/${id}`)
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between gap-4">
      <h1 class="font-display text-3xl text-navy">Formations</h1>
      <button class="btn btn-navy py-2" @click="editing = {}; Object.assign(form, empty())">Nouvelle</button>
    </div>

    <form v-if="editing" class="mt-6 grid gap-3 rounded-2xl bg-white p-6 shadow-soft md:grid-cols-2" @submit.prevent="save">
      <input v-model="form.slug" placeholder="slug" required />
      <input v-model="form.code" placeholder="code" required />
      <input v-model="form.title_fr" placeholder="Titre FR" required />
      <input v-model="form.title_en" placeholder="Title EN" required />
      <input v-model="form.tagline_fr" placeholder="Accroche FR" class="md:col-span-2" />
      <input v-model="form.tagline_en" placeholder="Tagline EN" class="md:col-span-2" />
      <textarea v-model="form.description_fr" rows="3" placeholder="Description FR" />
      <textarea v-model="form.description_en" rows="3" placeholder="Description EN" />
      <textarea v-model="form.obj_fr" rows="4" placeholder="Objectifs FR (1 par ligne)" />
      <textarea v-model="form.obj_en" rows="4" placeholder="Objectives EN (1 per line)" />
      <textarea v-model="form.mod_fr" rows="4" placeholder="Modules FR (1 par ligne)" />
      <textarea v-model="form.mod_en" rows="4" placeholder="Modules EN (1 per line)" />
      <textarea v-model="form.audience_fr" rows="2" placeholder="Public FR" />
      <textarea v-model="form.audience_en" rows="2" placeholder="Audience EN" />
      <textarea v-model="form.prerequisites_fr" rows="2" placeholder="Prérequis FR" />
      <textarea v-model="form.prerequisites_en" rows="2" placeholder="Prerequisites EN" />
      <input v-model="form.image_url" placeholder="Image URL" class="md:col-span-2" />
      <input v-model="form.category" placeholder="Catégorie" />
      <input v-model="form.sort_order" type="number" placeholder="Ordre" />
      <label class="flex items-center gap-2 text-sm"><input v-model="form.is_published" type="checkbox" class="w-auto" /> Publié</label>
      <label class="flex items-center gap-2 text-sm"><input v-model="form.is_featured" type="checkbox" class="w-auto" /> Mis en avant</label>
      <div class="flex gap-2 md:col-span-2">
        <button class="btn btn-wine">Enregistrer</button>
        <button type="button" class="btn btn-outline" @click="editing = null">Annuler</button>
      </div>
    </form>

    <div class="mt-6 overflow-x-auto rounded-2xl bg-white shadow-soft">
      <table class="w-full text-left text-sm">
        <thead class="text-xs uppercase text-mute">
          <tr>
            <th class="p-4">Code</th>
            <th>Titre</th>
            <th>Slug</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="r in rows" :key="String(r.id)" class="border-t border-navy/5">
            <td class="p-4 font-medium">{{ r.code }}</td>
            <td>{{ r.title_fr }}</td>
            <td class="text-mute">{{ r.slug }}</td>
            <td class="p-4 text-right">
              <button class="mr-3 text-navy" @click="editing = r; loadForm(r)">Modifier</button>
              <button class="text-red-600" @click="remove(String(r.id))">Supprimer</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
