<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { api } from '../lib/api'
import { useCatalog } from '../stores'
import { loc, type Locale } from '../types'

const { t, locale } = useI18n()
const route = useRoute()
const catalog = useCatalog()
const sent = ref(false)
const loading = ref(false)
const l = computed(() => locale.value as Locale)

const form = reactive({
  full_name: '',
  whatsapp: '',
  email: '',
  program_id: '',
  session_id: '',
  prior_level: '',
  format_preference: 'in_person',
  objective: '',
  privacy_accepted: false,
})

const sessionsForProgram = computed(() => {
  if (!form.program_id) return catalog.sessions
  return catalog.sessions.filter((s) => s.program_id === form.program_id)
})

watch(
  () => catalog.loaded,
  () => {
    const q = String(route.query.session || '')
    if (!q) return
    const s = catalog.sessions.find((x) => x.slug === q)
    if (s) {
      form.session_id = s.id
      form.program_id = s.program_id
    }
  },
  { immediate: true },
)

watch(
  () => form.program_id,
  (id) => {
    if (form.session_id && !sessionsForProgram.value.some((s) => s.id === form.session_id)) {
      form.session_id = ''
    }
    if (id && sessionsForProgram.value.length === 1) form.session_id = sessionsForProgram.value[0].id
  },
)

async function submit() {
  loading.value = true
  try {
    await api.post('/enrollments', {
      ...form,
      program_id: form.program_id || null,
      session_id: form.session_id || null,
    })
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="container-page max-w-3xl pb-24 pt-28">
    <p class="eyebrow">ACAD’EMY</p>
    <h1 class="mt-3 font-display text-4xl text-navy md:text-5xl">{{ t('enroll.title') }}</h1>
    <p class="mt-3 text-mute">{{ t('enroll.lead') }}</p>

    <div v-if="sent" class="mt-10 rounded-2xl bg-white p-8 shadow-soft">
      <h2 class="font-display text-3xl text-navy">{{ t('enroll.thanksTitle') }}</h2>
      <p class="mt-4 text-mute">{{ t('enroll.thanks') }}</p>
      <button class="btn btn-navy mt-6" @click="sent = false">{{ t('enroll.another') }}</button>
    </div>

    <form v-else class="mt-10 space-y-4 rounded-2xl bg-white p-6 shadow-soft md:p-8" @submit.prevent="submit">
      <div>
        <label class="field">{{ t('enroll.fullName') }}</label>
        <input v-model="form.full_name" required />
      </div>
      <div class="grid gap-4 md:grid-cols-2">
        <div>
          <label class="field">{{ t('enroll.whatsapp') }}</label>
          <input v-model="form.whatsapp" required />
        </div>
        <div>
          <label class="field">{{ t('enroll.email') }}</label>
          <input v-model="form.email" type="email" required />
        </div>
      </div>
      <div>
        <label class="field">{{ t('enroll.program') }}</label>
        <select v-model="form.program_id" required>
          <option value="" disabled>{{ t('enroll.program') }}</option>
          <option v-for="p in catalog.programs" :key="p.id" :value="p.id">{{ loc(p, l, 'title') }}</option>
        </select>
      </div>
      <div>
        <label class="field">{{ t('enroll.session') }}</label>
        <select v-model="form.session_id">
          <option value="">—</option>
          <option v-for="s in sessionsForProgram" :key="s.id" :value="s.id">{{ loc(s, l, 'title') }}</option>
        </select>
      </div>
      <div>
        <label class="field">{{ t('enroll.level') }}</label>
        <input v-model="form.prior_level" />
      </div>
      <div>
        <label class="field">{{ t('enroll.format') }}</label>
        <select v-model="form.format_preference">
          <option value="in_person">{{ t('enroll.inPerson') }}</option>
          <option value="online">{{ t('enroll.online') }}</option>
          <option value="hybrid">{{ t('enroll.hybrid') }}</option>
        </select>
      </div>
      <div>
        <label class="field">{{ t('enroll.objective') }}</label>
        <textarea v-model="form.objective" rows="4" />
      </div>
      <label class="flex items-start gap-3 text-sm text-mute">
        <input v-model="form.privacy_accepted" type="checkbox" required class="mt-1 w-auto" />
        <span>
          {{ t('enroll.privacy') }}
          <RouterLink to="/confidentialite" class="text-navy underline">{{ t('cta.privacy') }}</RouterLink>
        </span>
      </label>
      <button class="btn btn-wine w-full" :disabled="loading">
        {{ loading ? t('cta.sending') : t('enroll.submit') }}
      </button>
    </form>
  </main>
</template>
