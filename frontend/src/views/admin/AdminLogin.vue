<script setup lang="ts">
import { reactive, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { Eye, EyeOff, Lock, Mail } from '@lucide/vue'
import { api } from '../../lib/api'

const { t } = useI18n()
const router = useRouter()
const error = ref('')
const loading = ref(false)
const showPassword = ref(false)
const form = reactive({ email: '', password: '' })

async function submit() {
  error.value = ''
  loading.value = true
  try {
    const { data } = await api.post('/auth/login', form)
    localStorage.setItem('academy_token', data.access_token)
    localStorage.setItem('academy_admin', JSON.stringify({ name: data.name, email: data.email }))
    router.push('/admin')
  } catch {
    error.value = t('admin.loginError')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <main class="grid min-h-svh lg:grid-cols-2">
    <aside class="relative hidden overflow-hidden lg:block">
      <img src="/images/back-01.jpg" alt="" class="absolute inset-0 h-full w-full object-cover kenburns" />
      <div class="absolute inset-0 bg-gradient-to-t from-navy via-navy/75 to-navy/45" />
      <div class="relative z-10 flex h-full flex-col justify-between p-10 text-white">
        <RouterLink to="/" class="flex shrink-0 items-center gap-2.5">
        <span class="flex h-20 w-20 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm ring-1 ring-black/5">
          <img src="/images/academy-logo.jpg" alt=""  class="h-20 w-20 object-contain transition-transform scale-150" />
        </span>

      </RouterLink>
        <div class="max-w-md">
          <p class="eyebrow text-gold">{{ t('admin.loginKicker') }}</p>
          <h1 class="mt-4 font-display text-5xl leading-tight">{{ t('admin.loginTitle') }}</h1>
          <p class="mt-4 text-white/70">{{ t('admin.loginLead') }}</p>
        </div>
        <div class="flex items-center gap-3">
          <span class="rounded-md bg-white px-2 py-1">
            <img src="/images/lawapp-logo.jpg" alt="LawApp50 Group" class="h-9 w-auto object-contain" />
          </span>
          <p class="text-xs uppercase tracking-[0.16em] text-white/50">{{ t('parent') }}</p>
        </div>
      </div>
    </aside>

    <section class="relative flex items-center justify-center bg-cream px-5 py-12">
      <div class="pointer-events-none absolute inset-0 opacity-40" style="background-image: radial-gradient(#922b3e12 1px, transparent 1px); background-size: 22px 22px" />
      <form class="relative w-full max-w-[380px]" @submit.prevent="submit">
        <RouterLink to="/" class="mb-8 flex items-center gap-2 lg:hidden">
          <span class="flex h-11 w-11 items-center justify-center overflow-hidden rounded-xl bg-white shadow-sm">
            <img src="/images/academy-mark.jpg" alt="" class="h-20 w-20 object-contain transition-transform scale-150" />
          </span>
          <span class="font-display text-xl text-navy">Acad’Emy</span>
        </RouterLink>
        <p class="eyebrow">{{ t('admin.loginKicker') }}</p>
        <h2 class="mt-3 font-display text-3xl text-navy">{{ t('admin.login') }}</h2>
        <p class="mt-2 text-sm text-mute">{{ t('admin.loginHint') }}</p>

        <div class="mt-8">
          <label class="field" for="team-email">{{ t('admin.email') }}</label>
          <div class="relative">
            <Mail class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-mute" :size="15" />
            <input
              id="team-email"
              v-model="form.email"
              type="email"
              required
              autocomplete="username"
              class="pl-9"
              :placeholder="t('admin.emailPlaceholder')"
            />
          </div>
        </div>
        <div class="mt-3.5">
          <label class="field" for="team-password">{{ t('admin.password') }}</label>
          <div class="relative">
            <Lock class="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-mute" :size="15" />
            <input
              id="team-password"
              v-model="form.password"
              :type="showPassword ? 'text' : 'password'"
              required
              autocomplete="current-password"
              class="px-9"
              :placeholder="t('admin.passwordPlaceholder')"
            />
            <button
              type="button"
              class="absolute right-2.5 top-1/2 -translate-y-1/2 text-mute hover:text-navy"
              :aria-label="showPassword ? 'Hide password' : 'Show password'"
              @click="showPassword = !showPassword"
            >
              <EyeOff v-if="showPassword" :size="15" />
              <Eye v-else :size="15" />
            </button>
          </div>
        </div>
        <p v-if="error" class="mt-3 text-sm text-wine">{{ error }}</p>
        <button class="btn btn-wine mt-5 w-full py-2.5" :disabled="loading">
          {{ loading ? t('cta.sending') : t('admin.enter') }}
        </button>
        <p class="mt-6 text-center text-xs text-mute">
          <RouterLink to="/" class="hover:text-wine">{{ t('cta.back') }} — Acad’Emy</RouterLink>
        </p>
      </form>
    </section>
  </main>
</template>
