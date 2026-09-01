<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'
import { api } from '../lib/api'

const { t } = useI18n()
const sent = ref(false)
const loading = ref(false)
const form = reactive({
  company: '',
  contact_name: '',
  email: '',
  phone: '',
  audience: '',
  topics: '',
  message: '',
})

async function submit() {
  loading.value = true
  try {
    await api.post('/enterprise', form)
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="pb-24 pt-28">
    <div class="container-page">
      <SectionTitle :title="t('enterprise.title')" :lead="t('enterprise.lead')" />
      <p v-reveal class="mt-8 max-w-3xl text-lg leading-relaxed text-navy">{{ t('enterprise.intro') }}</p>
      <div class="mt-12 grid gap-6 md:grid-cols-3">
        <article v-for="n in 3" :key="n" v-reveal="n * 70" class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="font-display text-3xl text-gold">0{{ n }}</p>
          <h3 class="mt-3 text-lg text-navy">{{ t(`enterprise.f${n}t`) }}</h3>
          <p class="mt-2 text-sm text-mute">{{ t(`enterprise.f${n}d`) }}</p>
        </article>
      </div>
    </div>

    <section class="container-page mt-16">
      <div class="rounded-3xl bg-navy p-8 text-white md:p-12">
        <h2 class="font-display text-3xl">{{ t('enterprise.formT') }}</h2>
        <p v-if="sent" class="mt-6 text-gold">{{ t('enterprise.thanks') }}</p>
        <form v-else class="mt-8 grid gap-4 md:grid-cols-2" @submit.prevent="submit">
          <div>
            <label class="field text-white/60">{{ t('enterprise.company') }}</label>
            <input v-model="form.company" required class="bg-white/5 text-white" />
          </div>
          <div>
            <label class="field text-white/60">{{ t('enterprise.contact') }}</label>
            <input v-model="form.contact_name" required class="bg-white/5 text-white" />
          </div>
          <div>
            <label class="field text-white/60">{{ t('contact.email') }}</label>
            <input v-model="form.email" type="email" required class="bg-white/5 text-white" />
          </div>
          <div>
            <label class="field text-white/60">{{ t('contact.phone') }}</label>
            <input v-model="form.phone" class="bg-white/5 text-white" />
          </div>
          <div>
            <label class="field text-white/60">{{ t('enterprise.audience') }}</label>
            <input v-model="form.audience" class="bg-white/5 text-white" />
          </div>
          <div>
            <label class="field text-white/60">{{ t('enterprise.topics') }}</label>
            <input v-model="form.topics" class="bg-white/5 text-white" />
          </div>
          <div class="md:col-span-2">
            <label class="field text-white/60">{{ t('enterprise.message') }}</label>
            <textarea v-model="form.message" rows="4" class="bg-white/5 text-white" />
          </div>
          <button class="btn btn-gold md:col-span-2" :disabled="loading">
            {{ loading ? t('cta.sending') : t('cta.proposal') }}
          </button>
        </form>
      </div>
    </section>
  </main>
</template>
