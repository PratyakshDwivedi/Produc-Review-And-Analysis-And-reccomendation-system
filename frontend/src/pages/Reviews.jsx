import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { api } from '../services/api'
import ReviewCard from '../components/ReviewCard'
import { Loading, ErrorState, EmptyState, BackLink } from '../components/ui'
import { ASPECTS } from '../constants'

export default function Reviews() {
  const { id } = useParams()
  const [filters, setFilters] = useState({ sentiment: '', aspect: '', q: '', sort: 'recent', page: 1 })
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  function set(k, v) { setFilters((f) => ({ ...f, [k]: v, page: k === 'page' ? v : 1 })) }

  useEffect(() => {
    setLoading(true); setError(null)
    const params = { sort: filters.sort, page: filters.page, page_size: 8 }
    if (filters.sentiment) params.sentiment = filters.sentiment
    if (filters.aspect) params.aspect = filters.aspect
    if (filters.q) params.q = filters.q
    api.reviews(id, params).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false))
  }, [id, filters])

  const pages = data ? Math.ceil(data.total / data.page_size) : 1

  return (
    <div>
      <BackLink to={`/product/${id}`}>Back to analysis</BackLink>
      <h1 style={{ margin: '10px 0 16px' }}>Reviews explorer</h1>

      <div className="card" style={{ marginBottom: 16 }}>
        <div className="row">
          <input placeholder="Search in reviews…" value={filters.q} onChange={(e) => set('q', e.target.value)} style={{ maxWidth: 260 }} />
          <select value={filters.sentiment} onChange={(e) => set('sentiment', e.target.value)} style={{ maxWidth: 160 }}>
            <option value="">All sentiment</option><option>positive</option><option>neutral</option><option>negative</option>
          </select>
          <select value={filters.aspect} onChange={(e) => set('aspect', e.target.value)} style={{ maxWidth: 160 }}>
            <option value="">All aspects</option>{ASPECTS.map((a) => <option key={a} value={a}>{a}</option>)}
          </select>
          <select value={filters.sort} onChange={(e) => set('sort', e.target.value)} style={{ maxWidth: 170 }}>
            <option value="recent">Most recent</option><option value="rating_high">Rating: high → low</option><option value="rating_low">Rating: low → high</option>
          </select>
        </div>
      </div>

      {loading ? <Loading /> : error ? <ErrorState message={error} />
        : data.items.length === 0 ? <EmptyState message="No reviews match these filters." />
        : (
          <>
            <p className="muted">{data.total} matching reviews</p>
            <div className="grid cols-2">{data.items.map((r) => <ReviewCard key={r.review_id} review={r} />)}</div>
            {pages > 1 && (
              <div className="row" style={{ justifyContent: 'center', marginTop: 18 }}>
                <button className="btn ghost sm" disabled={filters.page <= 1} onClick={() => set('page', filters.page - 1)}>Prev</button>
                <span className="muted">Page {filters.page} / {pages}</span>
                <button className="btn ghost sm" disabled={filters.page >= pages} onClick={() => set('page', filters.page + 1)}>Next</button>
              </div>
            )}
          </>
        )}
    </div>
  )
}
