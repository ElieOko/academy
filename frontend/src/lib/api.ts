import axios from 'axios'

const DEFAULT_PRODUCTION_API = 'https://backend.acad-emy.com/api'

function apiBaseUrl(): string {
  const fromEnv = import.meta.env.VITE_API_URL?.trim()
  if (fromEnv) return fromEnv.replace(/\/$/, '')
  if (import.meta.env.PROD) return DEFAULT_PRODUCTION_API
  return '/api'
}

export const api = axios.create({
  baseURL: apiBaseUrl(),
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('academy_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})
