export type Locale = 'fr' | 'en'

export interface Program {
  id: string
  slug: string
  code: string
  title_fr: string
  title_en: string
  tagline_fr: string
  tagline_en: string
  description_fr: string
  description_en: string
  objectives: { fr: string; en: string }[]
  audience_fr: string
  audience_en: string
  modules: { fr: string; en: string }[]
  prerequisites_fr: string
  prerequisites_en: string
  image_url: string
  category: string
  is_featured: boolean
  sort_order: number
  sessions?: Session[]
}

export interface Session {
  id: string
  program_id: string
  slug: string
  title_fr: string
  title_en: string
  summary_fr: string
  summary_en: string
  start_date: string | null
  end_date: string | null
  duration_fr: string
  duration_en: string
  status: string
  tuition_usd: number
  enrollment_fee_usd: number
  format: string
  cta_fr: string
  cta_en: string
  is_highlighted: boolean
  max_seats: number | null
  program?: Program
}

export interface NewsItem {
  id: string
  slug: string
  title_fr: string
  title_en: string
  excerpt_fr: string
  excerpt_en: string
  content_fr: string
  content_en: string
  image_url: string
  category: string
  published_at: string | null
}

export interface Testimonial {
  id: string
  name: string
  role_fr: string
  role_en: string
  quote_fr: string
  quote_en: string
  photo_url: string
}

export interface ContactInfo {
  phone?: string
  whatsapp?: string
  email?: string
  address_fr?: string
  address_en?: string
  hours_fr?: string
  hours_en?: string
  maps_embed?: string
  maps_url?: string
  facebook?: string
  instagram?: string
  linkedin?: string
  parent?: string
}

export function loc<T extends Record<string, unknown>>(obj: T, locale: Locale, key: string): string {
  const k = `${key}_${locale}`
  const fallback = `${key}_fr`
  return String(obj[k] ?? obj[fallback] ?? '')
}
