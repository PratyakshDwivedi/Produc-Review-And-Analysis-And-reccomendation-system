import { useEffect, useState } from 'react'
import { api } from '../services/api'
import ProductCard from '../components/ProductCard'
import { Loading, ErrorState, EmptyState, PageHead } from '../components/ui'

export default function Search() {
  const [q, setQ] = useState('')
  const [category, setCategory] = useState('')
  const [categories, setCategories] = useState([])
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => { api.categories().then(setCategories).catch(() => {}) }, [])

  useEffect(() => {
    const t = setTimeout(() => {
      setLoading(true); setError(null)
      api.products(q, category).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false))
    }, 250)
    return () => clearTimeout(t)
  }, [q, category])

  return (
    <div>
      <PageHead title="Product search">Search by name or brand and filter by category.</PageHead>
      <div className="row" style={{ marginBottom: 18 }}>
        <input placeholder="Search products…" value={q} onChange={(e) => setQ(e.target.value)} style={{ maxWidth: 360 }} />
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ maxWidth: 220 }}>
          <option value="">All categories</option>
          {categories.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>
      {loading ? <Loading /> : error ? <ErrorState message={error} />
        : data.length === 0 ? <EmptyState message="No products match your search." />
        : <div className="grid cols-4">{data.map((p) => <ProductCard key={p.product_id} product={p} />)}</div>}
    </div>
  )
}
