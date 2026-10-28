import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { Loading, ErrorState, PageHead, Stars } from '../components/ui'

export default function Rankings() {
  const [categories, setCategories] = useState([])
  const [category, setCategory] = useState('')
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => { api.categories().then(setCategories).catch(() => {}) }, [])
  useEffect(() => {
    setLoading(true); setError(null)
    api.rankings(category).then(setData).catch((e) => setError(e.message)).finally(() => setLoading(false))
  }, [category])

  return (
    <div>
      <PageHead title="Category rankings">
        Ranked by a confidence-adjusted rating so products with very few reviews can't dominate.
      </PageHead>
      <div className="row" style={{ marginBottom: 16 }}>
        <select value={category} onChange={(e) => setCategory(e.target.value)} style={{ maxWidth: 220 }}>
          <option value="">All categories</option>
          {categories.map((c) => <option key={c} value={c}>{c}</option>)}
        </select>
      </div>
      {loading ? <Loading /> : error ? <ErrorState message={error} /> : (
        <>
          <p className="notice">{data.methodology}</p>
          <table className="compare">
            <thead><tr><th>#</th><th>Product</th><th>Category</th><th>Rating</th><th>Adjusted</th><th>Positive %</th><th>Score</th></tr></thead>
            <tbody>
              {data.ranking.map((r) => (
                <tr key={r.product_id}>
                  <td>{r.rank}</td>
                  <td><Link to={`/product/${r.product_id}`}>{r.name}</Link></td>
                  <td>{r.category}</td>
                  <td><Stars value={r.rating} /> {r.rating}</td>
                  <td>{r.adjusted_rating}</td>
                  <td>{Math.round(r.positive_share * 100)}%</td>
                  <td><span className="chip pos">{r.rank_score}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  )
}
