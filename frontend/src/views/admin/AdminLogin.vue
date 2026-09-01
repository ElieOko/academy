<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { api } from '../../lib/api'

const { t } = useI18n()
const router = useRouter()
const error = ref('')
const loading = ref(false)
const form = reactive({ email: 'admin@acad-emy.com', password: '' })

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/login', form)
    localStorage.setItem('academy_token', data.access_token)
    localStorage.setItem('academy_admin', JSON.stringify({ name: data.name, email: data.email }))
    router.push('/admin')
  } catch {
    error.value = 'Identifiants incorrects.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="flex min-h-screen items-center justify-center bg-navy px-5">
    <form class="w-full max-w-sm rounded-2xl bg-white p-8" @submit.prevent="submit">
      <p class="font-display text-3xl text-navy">Acad’Emy</p>
      <p class="mt-1 text-sm text-mute">{{ t('admin.login') }}</p>
      <div class="mt-6">
        <label class="field">{{ t('admin.email') }}</label>
        <input v-model="form.email" type="email" required />
      </div>
      <div class="mt-4">
        <label class="field">{{ t('admin.password') }}</label>
        <input v-model="form.password" type="password" required />
      </div>
      <p v-if="error" class="mt-3 text-sm text-red-600">{{ error }}</p>
      <button class="btn btn-navy mt-6 w-full" :disabled="loading">{{ t('admin.enter') }}</button>
    </form>
  </main>
</template>
