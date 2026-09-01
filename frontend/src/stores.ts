import { createPinia, defineStore } from 'pinia'
import { api } from './lib/api'
import type { ContactInfo, NewsItem, Program, Session, Testimonial } from './types'

export const pinia = createPinia()

export const useCatalog = defineStore('catalog', {
  state: () => ({
    programs: [] as Program[],
    sessions: [] as Session[],
    news: [] as NewsItem[],
    testimonials: [] as Testimonial[],
    contact: {} as ContactInfo,
    loaded: false,
  }),
  getters: {
    highlighted: (s) => s.sessions.filter((x) => x.is_highlighted),
    englishProgram: (s) => s.programs.find((p) => p.slug === 'anglais' || p.code === 'ENG'),
  },
  actions: {
    async load() {
      if (this.loaded) return
      const [programs, sessions, news, testimonials, contact] = await Promise.all([
        api.get('/programs'),
        api.get('/sessions'),
        api.get('/news'),
        api.get('/testimonials'),
        api.get('/settings/contact'),
      ])
      this.programs = programs.data
      this.sessions = sessions.data
      this.news = news.data
      this.testimonials = testimonials.data
      this.contact = contact.data
      this.loaded = true
    },
  },
})
