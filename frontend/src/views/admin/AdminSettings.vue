<script setup lang="ts">
import { onMounted, reactive } from 'vue'
import { api } from '../../lib/api'

const form = reactive({
  phone: '',
  whatsapp: '',
  email: '',
  address_fr: '',
  address_en: '',
  hours_fr: '',
  hours_en: '',
  maps_embed: '',
  maps_url: '',
  facebook: '',
  instagram: '',
  linkedin: '',
  parent: 'LawApp Group50',
})
const saved = reactive({ ok: false })

onMounted(async () => {
  const { data } = await api.get('/admin/settings/contact')
  Object.assign(form, data)
})

async function save() {
  await api.put('/admin/settings/contact', { value: { ...form } })
  saved.ok = true
  setTimeout(() => (saved.ok = false), 2000)
}
</script>

<template>
  <div>
    <h1 class="font-display text-3xl text-navy">Paramètres de contact</h1>
    <form class="mt-6 grid max-w-2xl gap-3 rounded-2xl bg-white p-6 shadow-soft" @submit.prevent="save">
      <input v-model="form.phone" placeholder="Téléphone" />
      <input v-model="form.whatsapp" placeholder="WhatsApp (243…)" />
      <input v-model="form.email" placeholder="E-mail" />
      <input v-model="form.address_fr" placeholder="Adresse FR" />
      <input v-model="form.address_en" placeholder="Address EN" />
      <textarea v-model="form.hours_fr" rows="3" placeholder="Horaires FR" />
      <textarea v-model="form.hours_en" rows="3" placeholder="Hours EN" />
      <input v-model="form.maps_embed" placeholder="Google Maps embed URL" />
      <input v-model="form.maps_url" placeholder="Google Maps link" />
      <input v-model="form.facebook" placeholder="Facebook" />
      <input v-model="form.instagram" placeholder="Instagram" />
      <input v-model="form.linkedin" placeholder="LinkedIn" />
      <button class="btn btn-gold">Enregistrer</button>
      <p v-if="saved.ok" class="text-sm text-emerald-700">Enregistré.</p>
    </form>
  </div>
</template>
