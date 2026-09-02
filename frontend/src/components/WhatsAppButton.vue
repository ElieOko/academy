<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useCatalog } from '../stores'

const { locale } = useI18n()
const catalog = useCatalog()
const href = computed(() => {
  const n = catalog.contact.whatsapp || '243810000243'
  const text =
    locale.value === 'en'
      ? 'Hello ACAD’EMY, I would like information about your programs.'
      : 'Bonjour ACAD’EMY, je souhaite des informations sur vos formations.'
  return `https://wa.me/${n}?text=${encodeURIComponent(text)}`
})
</script>

<template>
  <a
    :href="href"
    target="_blank"
    rel="noreferrer"
    class="fixed bottom-5 right-5 z-50 flex h-14 w-14 items-center justify-center rounded-full bg-[#25D366] text-white shadow-lg transition hover:scale-105"
    aria-label="WhatsApp"
  >
    <svg viewBox="0 0 24 24" class="h-7 w-7" fill="currentColor">
      <path
        d="M20.5 3.5A11 11 0 0 0 2.1 17.2L1 23l6-1.6A11 11 0 0 0 20.5 3.5Zm-8.5 17a9.1 9.1 0 0 1-4.6-1.3l-.3-.2-3.5.9.9-3.4-.2-.3a9.1 9.1 0 1 1 7.7 4.3Zm5-6.8c-.3-.1-1.6-.8-1.9-.9s-.4-.1-.6.1-.7.9-.8 1-.3.2-.6.1a7.4 7.4 0 0 1-2.2-1.4 8.2 8.2 0 0 1-1.5-1.9c-.2-.3 0-.4.1-.6l.5-.6.3-.4v-.4c0-.2-.6-1.5-.8-2s-.4-.5-.6-.5h-.5c-.2 0-.5.1-.8.4s-1 1-1 2.4 1 2.8 1.2 3 2 3.1 4.9 4.2a11 11 0 0 0 1.9.6c.8.2 1.5.2 2.1.1.6-.1 1.6-.7 1.8-1.3s.2-1.2.1-1.3-.2-.2-.5-.3Z"
      />
    </svg>
  </a>
</template>
