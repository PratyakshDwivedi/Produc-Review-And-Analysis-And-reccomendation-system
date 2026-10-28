import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { Loading, ErrorState, PageHead, ScoreChip, Stars, EmptyState } from '../components/ui'
import { ASPECTS } from '../constants'

export default function Compare() {
  const [products, setProducts] = useState([])
  const [selected, setSelected] = useState([])
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => { api.products().then(setProducts).catch(() => {}) }, [])

  function toggle(id) {
    setSelected((s) => s.includes(id) ? s.filter((x) => x !== id) : s.length >= 3 ? s : [...s, id])
  }

  useEffect(() => {
    if (selected.length < 2) { setData(null); return }
    setLoading(true); setError(null)
    api.compare(selected).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false))
  }, [selected])

  const rows = data?.products || []

  return (
    <div>
      <PageHead title="Compare products">Select 2-3 products to compare side by side.</PageHead>

      <div className="card" style={{ marginBottom: 18 }}>
        <div className="tag-list">
          {products.map((p) => (
            <button key={p.product_id} onClick={() => toggle(p.product_id)}
              className={`chip ${selected.includes(p.product_id) ? 'pos' : ''}`}
              style={{ cursor: 'pointer', border: 0 }} disabled={!selected.includes(p.product_id) && selected.length >= 3}>
              {p.name}
            </button>
          ))}
        </div>
        <p className="muted" style={{ margin: '10px 0 0', fontSize: '0.82rem' }}>{selected.length}/3 selected</p>
      </div>

      {selected.length < 2 && <EmptyState message="Pick at least two products to compare." />}
      {loading && <Loading />}
      {error && <ErrorState message={error} />}

      {rows.length >= 2 && (
        <div style={{ overflowX: 'auto' }}>
          <table className="compare">
            <thead>
              <tr><th>Attribute</th>{rows.map((r) => <th key={r.product_id}>{r.name}</th>)}</tr>
            </thead>
            <tbody>
              <tr><td className="rowhead">Brand</td>{rows.map((r) => <td key={r.product_id}>{r.brand}</td>)}</tr>
              <tr><td className="rowhead">Price</td>{rows.map((r) => <td key={r.product_id} className="price">${r.price}</td>)}</tr>
              <tr><td className="rowhead">Rating</td>{rows.map((r) => <td key={r.product_id}><Stars value={r.rating} /> {r.rating}</td>)}</tr>
              <tr><td className="rowhead">Reviews</td>{rows.map((r) => <td key={r.product_id}>{r.review_count}</td>)}</tr>
              <tr><td className="rowhead">Positive %</td>{rows.map((r) => <td key={r.product_id}>{Math.round(r.positive_share * 100)}%</td>)}</tr>
              {ASPECTS.map((asp) => {
                if (!rows.some((r) => asp in r.aspects)) return null
                return (
                  <tr key={asp}><td className="rowhead">{asp}</td>
                    {rows.map((r) => <td key={r.product_id}>{asp in r.aspects ? <ScoreChip score={r.aspects[asp]} /> : <span className="muted">—</span>}</td>)}
                  </tr>
                )
              })}
              <tr><td className="rowhead">Strengths</td>{rows.map((r) => <td key={r.product_id}>{r.strengths.join(', ') || '—'}</td>)}</tr>
              <tr><td className="rowhead">Weaknesses</td>{rows.map((r) => <td key={r.product_id}>{r.weaknesses.join(', ') || '—'}</td>)}</tr>
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
