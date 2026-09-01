<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import SectionTitle from '../components/SectionTitle.vue'
import { api } from '../lib/api'
import { useCatalog } from '../stores'
import { loc, type Locale } from '../types'

const { t, locale } = useI18n()
const catalog = useCatalog()
const sent = ref(false)
const loading = ref(false)
const form = reactive({ name: '', email: '', phone: '', message: '' })
const l = computed(() => locale.value as Locale)
const whatsapp = computed(() => `https://wa.me/${catalog.contact.whatsapp || '243810000243'}`)

async function submit() {
  loading.value = true
  try {
    await api.post('/contact', form)
    sent.value = true
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="container-page pb-24 pt-28">
    <SectionTitle :title="t('contact.title')" :lead="t('contact.lead')" />
    <div class="mt-12 grid gap-10 lg:grid-cols-2">
      <div class="space-y-5">
        <article class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="eyebrow">{{ t('contact.phone') }}</p>
          <a :href="`tel:${catalog.contact.phone}`" class="mt-2 block text-lg">{{ catalog.contact.phone }}</a>
        </article>
        <article class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="eyebrow">{{ t('contact.whatsapp') }}</p>
          <a :href="whatsapp" target="_blank" class="mt-2 block text-lg text-emerald-700">WhatsApp</a>
        </article>
        <article class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="eyebrow">{{ t('contact.email') }}</p>
          <a :href="`mailto:${catalog.contact.email}`" class="mt-2 block text-lg">{{ catalog.contact.email }}</a>
        </article>
        <article class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="eyebrow">{{ t('contact.address') }}</p>
          <p class="mt-2">{{ loc(catalog.contact as never, l, 'address') }}</p>
        </article>
        <article class="rounded-2xl bg-white p-6 shadow-soft">
          <p class="eyebrow">{{ t('contact.hours') }}</p>
          <p class="mt-2 whitespace-pre-line text-sm">{{ loc(catalog.contact as never, l, 'hours') }}</p>
        </article>
        <div class="flex gap-4 text-sm">
          <a v-if="catalog.contact.facebook" :href="catalog.contact.facebook" target="_blank">Facebook</a>
          <a v-if="catalog.contact.instagram" :href="catalog.contact.instagram" target="_blank">Instagram</a>
          <a v-if="catalog.contact.linkedin" :href="catalog.contact.linkedin" target="_blank">LinkedIn</a>
        </div>
      </div>
      <div>
        <iframe
          v-if="catalog.contact.maps_embed"
          :src="catalog.contact.maps_embed"
          class="mb-6 h-56 w-full rounded-2xl border-0"
          loading="lazy"
        />
        <div class="rounded-2xl bg-white p-6 shadow-soft">
          <h2 class="font-display text-2xl">{{ t('contact.formT') }}</h2>
          <p v-if="sent" class="mt-4 text-emerald-800">{{ t('contact.thanks') }}</p>
          <form v-else class="mt-5 space-y-4" @submit.prevent="submit">
            <div>
              <label class="field">{{ t('contact.name') }}</label>
              <input v-model="form.name" required />
            </div>
            <div>
              <label class="field">{{ t('contact.email') }}</label>
              <input v-model="form.email" type="email" required />
            </div>
            <div>
              <label class="field">{{ t('contact.phone') }}</label>
              <input v-model="form.phone" />
            </div>
            <div>
              <label class="field">{{ t('contact.message') }}</label>
              <textarea v-model="form.message" rows="4" required />
            </div>
            <button class="btn btn-navy w-full" :disabled="loading">
              {{ loading ? t('cta.sending') : t('cta.send') }}
            </button>
          </form>
        </div>
      </div>
    </div>
  </main>
</template>
