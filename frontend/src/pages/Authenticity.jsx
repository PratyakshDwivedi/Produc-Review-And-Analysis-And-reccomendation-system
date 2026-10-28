import { useParams } from 'react-router-dom'
import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { Loading, ErrorState, BackLink } from '../components/ui'

export default function Authenticity() {
  const { id } = useParams()
  const { data, error, loading, reload } = useFetch(() => api.authenticity(id), [id])

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />

  const flagged = data.reviews.filter((r) => r.risk_category !== 'low')

  return (
    <div>
      <BackLink to={`/product/${id}`}>Back to analysis</BackLink>
      <h1 style={{ margin: '10px 0 8px' }}>Review authenticity</h1>
      <p className="notice">{data.note}</p>
      <div className="grid cols-3" style={{ margin: '16px 0' }}>
        <div className="card"><div className="muted">Reviews analyzed</div><div style={{ fontSize: '1.6rem' }}>{data.total}</div></div>
        <div className="card"><div className="muted">Flagged</div><div style={{ fontSize: '1.6rem' }}>{data.flagged_count}</div></div>
        <div className="card"><div className="muted">Flagged share</div><div style={{ fontSize: '1.6rem' }}>{Math.round(data.flagged_share * 100)}%</div></div>
      </div>

      <h3>Flagged reviews</h3>
      {flagged.length === 0 ? <p className="muted">No reviews were flagged as higher risk.</p> : (
        <table className="compare">
          <thead><tr><th>Review ID</th><th>Risk</th><th>Score</th><th>Signals</th></tr></thead>
          <tbody>
            {flagged.map((r) => (
              <tr key={r.review_id}>
                <td className="rowhead">{r.review_id}</td>
                <td><span className={`chip risk-${r.risk_category}`}>{r.risk_category}</span></td>
                <td>{r.risk_score}</td>
                <td>{r.signals.join('; ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  )
}
