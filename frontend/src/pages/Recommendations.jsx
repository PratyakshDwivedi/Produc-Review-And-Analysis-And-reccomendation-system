import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { Loading, ErrorState, PageHead, Stars } from '../components/ui'

const EXAMPLES = [
  'A phone with a great camera and battery for gaming under $800',
  'Budget headphones with good sound and comfort',
  'A premium laptop with strong performance and display',
]

export default function Recommendations() {
  const [query, setQuery] = useState('')
  const [res, setRes] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function run(q) {
    const text = (q ?? query).trim()
    if (!text) return
    setQuery(text); setLoading(true); setError(null); setRes(null)
    try { setRes(await api.recommend(text)) } catch (e) { setError(e.message) } finally { setLoading(false) }
  }

  return (
    <div>
      <PageHead title="Natural-language recommendations">
        Describe what you want. We match it to products using aspect sentiment, ratings and review evidence.
      </PageHead>

      <div className="card">
        <div className="row" style={{ flexWrap: 'nowrap' }}>
          <input placeholder="e.g. a phone with great camera and battery under $700"
            value={query} onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && run()} />
          <button className="btn" onClick={() => run()} disabled={loading}>Recommend</button>
        </div>
        <div className="tag-list" style={{ marginTop: 10 }}>
          {EXAMPLES.map((ex) => <button key={ex} className="chip" style={{ cursor: 'pointer', border: 0 }} onClick={() => run(ex)}>{ex}</button>)}
        </div>
      </div>

      {loading && <Loading label="Scoring products…" />}
      {error && <ErrorState message={error} />}

      {res && (
        <div style={{ marginTop: 18 }}>
          <p className="notice">{res.note}</p>
          <p className="muted">Detected: aspects [{res.parsed.aspects.join(', ') || 'none'}]
            {res.parsed.budget ? `, budget $${res.parsed.budget}` : ''}
            {res.parsed.categories.length ? `, category ${res.parsed.categories.join(', ')}` : ''}</p>
          <div className="grid cols-2">
            {res.results.map((r) => (
              <div className="card" key={r.product_id}>
                <div className="spread">
                  <Link to={`/product/${r.product_id}`}><strong>{r.name}</strong></Link>
                  <span className="chip pos">Match {r.match_score}</span>
                </div>
                <div className="muted" style={{ margin: '4px 0' }}>${r.price} · <Stars value={r.rating} /> {r.rating}</div>
                {r.matched_preferences.length > 0 && (
                  <div className="tag-list" style={{ marginBottom: 8 }}>
                    {r.matched_preferences.map((m) => <span key={m} className="chip pos">{m}</span>)}
                  </div>
                )}
                <strong style={{ fontSize: '0.85rem' }}>Why this matches</strong>
                <ul style={{ margin: '6px 0', paddingLeft: 18, fontSize: '0.88rem' }}>
                  {r.reasons.map((reason, i) => <li key={i}>{reason}</li>)}
                </ul>
                {r.evidence.length > 0 && (
                  <>
                    <strong style={{ fontSize: '0.85rem' }}>Review evidence</strong>
                    {r.evidence.map((e, i) => <p key={i} className="muted" style={{ fontSize: '0.85rem', margin: '4px 0' }}>“{e}”</p>)}
                  </>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
