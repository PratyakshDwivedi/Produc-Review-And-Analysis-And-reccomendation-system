import { Link, useParams } from 'react-router-dom'
import { Heart, LineChart, ShieldCheck, Tag } from 'lucide-react'
import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { useAuth } from '../context/AuthContext'
import { Loading, ErrorState, Stars, ScoreChip, BackLink } from '../components/ui'
import { SentimentPie, AspectBars } from '../components/charts'

export default function ProductAnalysis() {
  const { id } = useParams()
  const { user } = useAuth()
  const { data, error, loading, reload } = useFetch(() => api.analysis(id), [id])

  if (loading) return <Loading label="Analyzing reviews…" />
  if (error) return <ErrorState message={error} onRetry={reload} />

  const a = data
  async function addWishlist() {
    try { await api.addWishlist(id); alert('Added to wishlist') } catch (e) { alert(e.message) }
  }

  return (
    <div>
      <BackLink to="/search">Back to search</BackLink>
      <div className="spread" style={{ margin: '10px 0 20px' }}>
        <div>
          <h1 style={{ marginBottom: 4 }}>{a.name}</h1>
          <div className="muted">{a.brand} · {a.category}</div>
        </div>
        <div className="row">
          {user && <button className="btn ghost sm" onClick={addWishlist}><Heart size={14} /> Wishlist</button>}
          <Link className="btn ghost sm" to={`/product/${id}/reviews`}>Reviews</Link>
          <Link className="btn ghost sm" to={`/product/${id}/trends`}><LineChart size={14} /> Trends</Link>
          <Link className="btn ghost sm" to={`/product/${id}/authenticity`}><ShieldCheck size={14} /> Authenticity</Link>
          <Link className="btn ghost sm" to={`/product/${id}/price`}><Tag size={14} /> Price</Link>
        </div>
      </div>

      <div className="grid cols-4" style={{ marginBottom: 18 }}>
        <div className="card"><div className="muted">Price</div><div style={{ fontSize: '1.5rem' }} className="price">${a.price}</div></div>
        <div className="card"><div className="muted">Rating</div><div style={{ fontSize: '1.5rem' }}>{a.rating} <Stars value={a.rating} /></div></div>
        <div className="card"><div className="muted">Reviews</div><div style={{ fontSize: '1.5rem' }}>{a.review_count}</div></div>
        <div className="card"><div className="muted">Positive</div><div style={{ fontSize: '1.5rem' }}>{Math.round(a.positive_share * 100)}%</div></div>
      </div>

      <div className="grid cols-2">
        <div className="card">
          <h3>Sentiment distribution</h3>
          <SentimentPie distribution={a.sentiment_distribution} />
          <div className="row" style={{ justifyContent: 'center' }}>
            <span className="chip pos">Positive {a.sentiment_distribution.positive}</span>
            <span className="chip neu">Neutral {a.sentiment_distribution.neutral}</span>
            <span className="chip neg">Negative {a.sentiment_distribution.negative}</span>
          </div>
        </div>
        <div className="card">
          <h3>AI review summary</h3>
          <p>{a.summary.summary}</p>
          {a.keywords?.length > 0 && (
            <div className="tag-list">{a.keywords.slice(0, 8).map((k) => <span key={k} className="chip">{k}</span>)}</div>
          )}
        </div>
      </div>

      <div className="card" style={{ marginTop: 18 }}>
        <h3>Aspect sentiment</h3>
        <AspectBars aspects={a.aspects} />
      </div>

      <div className="grid cols-2" style={{ marginTop: 18 }}>
        <div className="card">
          <h3>Strengths</h3>
          {a.strengths.length ? <div className="tag-list">{a.strengths.map((s) => <span key={s} className="chip pos">{s}</span>)}</div>
            : <p className="muted">No standout strengths from the available reviews.</p>}
        </div>
        <div className="card">
          <h3>Weaknesses</h3>
          {a.weaknesses.length ? <div className="tag-list">{a.weaknesses.map((s) => <span key={s} className="chip neg">{s}</span>)}</div>
            : <p className="muted">No recurring weaknesses from the available reviews.</p>}
        </div>
      </div>

      <div className="card" style={{ marginTop: 18 }}>
        <h3>Aspect details</h3>
        <table className="compare">
          <thead><tr><th>Aspect</th><th>Score</th><th>Positive</th><th>Neutral</th><th>Negative</th><th>Mentions</th></tr></thead>
          <tbody>
            {a.aspects.map((r) => (
              <tr key={r.aspect}>
                <td className="rowhead">{r.aspect}</td>
                <td><ScoreChip score={r.score} /></td>
                <td>{r.positive}</td><td>{r.neutral}</td><td>{r.negative}</td><td>{r.total}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}
