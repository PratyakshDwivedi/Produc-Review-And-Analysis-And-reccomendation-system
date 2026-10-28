// API client for the FastAPI backend. Relative paths go through the Vite proxy
// in dev and the same origin in production (single-server / Vercel).
const BASE = import.meta.env.VITE_API_BASE || ''

let token = null
try { token = localStorage.getItem('token') } catch { /* ignore */ }

export function setToken(t) {
  token = t
  try { t ? localStorage.setItem('token', t) : localStorage.removeItem('token') } catch { /* ignore */ }
}

async function request(path, { method = 'GET', body, auth = false } = {}) {
  const headers = {}
  if (body !== undefined) headers['Content-Type'] = 'application/json'
  if (auth && token) headers['Authorization'] = `Bearer ${token}`
  const res = await fetch(`${BASE}${path}`, {
    method, headers, body: body !== undefined ? JSON.stringify(body) : undefined,
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) throw new Error(data.detail || `Request failed (${res.status})`)
  return data
}

export const api = {
  // catalog
  health: () => request('/health'),
  categories: () => request('/api/categories'),
  products: (q, category) => request(`/api/products?${new URLSearchParams(
    { ...(q ? { q } : {}), ...(category ? { category } : {}) })}`),
  product: (id) => request(`/api/products/${id}`),
  reviews: (id, params = {}) => request(`/api/reviews/${id}?${new URLSearchParams(params)}`),
  compare: (ids) => request(`/api/compare?ids=${ids.join(',')}`),

  // analysis
  analysis: (id) => request(`/api/analysis/${id}`),
  sentiment: (id) => request(`/api/analysis/${id}/sentiment`),
  aspects: (id) => request(`/api/analysis/${id}/aspects`),
  summary: (id) => request(`/api/analysis/${id}/summary`),
  trends: (id) => request(`/api/analysis/${id}/trends`),
  authenticity: (id) => request(`/api/analysis/${id}/authenticity`),
  predictRating: (text) => request('/api/analysis/predict-rating', { method: 'POST', body: { text } }),
  transformerStatus: () => request('/api/analysis/transformer/status'),
  transformerSentiment: (text) => request('/api/analysis/transformer/sentiment', { method: 'POST', body: { text } }),

  // recommend
  recommend: (query, top_k = 5) => request('/api/recommend', { method: 'POST', body: { query, top_k } }),
  rankings: (category, aspects) => request(`/api/rankings?${new URLSearchParams(
    { ...(category ? { category } : {}), ...(aspects ? { preferred_aspects: aspects } : {}) })}`),
  personalized: () => request('/api/personalized', { auth: true }),

  // auth
  register: (email, password, name) => request('/api/auth/register', { method: 'POST', body: { email, password, name } }),
  login: (email, password) => request('/api/auth/login', { method: 'POST', body: { email, password } }),
  me: () => request('/api/auth/me', { auth: true }),
  updateAccount: (name) => request('/api/auth/account', { method: 'PUT', body: { name }, auth: true }),

  // account
  wishlist: () => request('/api/wishlist', { auth: true }),
  addWishlist: (product_id) => request('/api/wishlist', { method: 'POST', body: { product_id }, auth: true }),
  removeWishlist: (id) => request(`/api/wishlist/${id}`, { method: 'DELETE', auth: true }),
  getPreferences: () => request('/api/preferences', { auth: true }),
  setPreferences: (prefs) => request('/api/preferences', { method: 'PUT', body: prefs, auth: true }),
  priceHistory: (id) => request(`/api/price/${id}`),
  alerts: () => request('/api/alerts', { auth: true }),
  createAlert: (product_id, target_price) => request('/api/alerts', { method: 'POST', body: { product_id, target_price }, auth: true }),
  updateAlert: (id, patch) => request(`/api/alerts/${id}`, { method: 'PUT', body: patch, auth: true }),
  deleteAlert: (id) => request(`/api/alerts/${id}`, { method: 'DELETE', auth: true }),
  notifications: () => request('/api/notifications', { auth: true }),
  readNotification: (id) => request(`/api/notifications/${id}/read`, { method: 'POST', auth: true }),
  readAllNotifications: () => request('/api/notifications/read-all', { method: 'POST', auth: true }),

  // chatbot
  chat: (message, history = []) => request('/api/chat', { method: 'POST', body: { message, history } }),
}
