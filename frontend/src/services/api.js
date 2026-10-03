// Thin API client for the FastAPI backend.
// Uses relative paths so the Vite dev proxy (see vite.config.js) forwards
// requests to the backend. Override with VITE_API_BASE in production.
const BASE = import.meta.env.VITE_API_BASE || ''

async function get(path) {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`Request failed: ${res.status}`)
  return res.json()
}

export const getHealth = () => get('/health')
export const getProducts = (q) => get(`/api/products${q ? `?q=${encodeURIComponent(q)}` : ''}`)
export const getReviews = (productId) => get(`/api/reviews/${productId}`)
