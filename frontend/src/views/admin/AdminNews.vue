<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../../lib/api'

const rows = ref<Record<string, unknown>[]>([])
const editing = ref<Record<string, unknown> | null>(null)
const form = reactive({
  slug: '',
  title_fr: '',
  title_en: '',
  excerpt_fr: '',
  excerpt_en: '',
  content_fr: '',
  content_en: '',
  image_url: '',
  category: 'news',
  is_published: true,
})

async function refresh() {
  rows.value = (await api.get('/admin/news')).data
}
onMounted(refresh)

function fill(r: Record<string, unknown> = {}) {
  editing.value = r
  Object.assign(form, {
    slug: r.slug || '',
    title_fr: r.title_fr || '',
    title_en: r.title_en || '',
    excerpt_fr: r.excerpt_fr || '',
    excerpt_en: r.excerpt_en || '',
    content_fr: r.content_fr || '',
    content_en: r.content_en || '',
    image_url: r.image_url || '',
    category: r.category || 'news',
    is_published: r.is_published !== false,
  })
}

async function save() {
  if (editing.value?.id) await api.put(`/admin/news/${editing.value.id}`, form)
  else await api.post('/admin/news', form)
  editing.value = null
  await refresh()
}

async function remove(id: string) {
  if (!confirm('Supprimer ?')) return
  await api.delete(`/admin/news/${id}`)
  await refresh()
}
</script>

<template>
  <div>
    <div class="flex items-center justify-between">
      <h1 class="font-display text-3xl text-navy">Actualités</h1>
      <button class="btn btn-navy py-2" @click="fill()">Nouvelle</button>
    </div>
    <form v-if="editing" class="mt-6 grid gap-3 rounded-2xl bg-white p-6 shadow-soft md:grid-cols-2" @submit.prevent="save">
      <input v-model="form.slug" placeholder="slug" required />
      <input v-model="form.category" placeholder="catégorie" />
      <input v-model="form.title_fr" placeholder="Titre FR" required />
      <input v-model="form.title_en" placeholder="Title EN" required />
      <textarea v-model="form.excerpt_fr" rows="2" placeholder="Extrait FR" />
      <textarea v-model="form.excerpt_en" rows="2" placeholder="Excerpt EN" />
      <textarea v-model="form.content_fr" rows="6" placeholder="Contenu FR" />
      <textarea v-model="form.content_en" rows="6" placeholder="Content EN" />
      <input v-model="form.image_url" placeholder="Image URL" class="md:col-span-2" />
      <label class="flex items-center gap-2 text-sm"><input v-model="form.is_published" type="checkbox" class="w-auto" /> Publié</label>
      <div class="flex gap-2 md:col-span-2">
        <button class="btn btn-wine">Enregistrer</button>
        <button type="button" class="btn btn-outline" @click="editing = null">Annuler</button>
      </div>
    </form>
    <div class="mt-6 space-y-3">
      <article v-for="r in rows" :key="String(r.id)" class="flex items-center justify-between rounded-2xl bg-white p-4 shadow-soft">
        <div>
          <p class="font-medium">{{ r.title_fr }}</p>
          <p class="text-xs text-mute">{{ r.slug }} · {{ r.category }}</p>
        </div>
        <div>
          <button class="mr-3" @click="fill(r)">Modifier</button>
          <button class="text-red-600" @click="remove(String(r.id))">Supprimer</button>
        </div>
      </article>
    </div>
  </div>
</template>
