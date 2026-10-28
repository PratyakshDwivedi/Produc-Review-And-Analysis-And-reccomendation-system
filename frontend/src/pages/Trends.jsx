import { useParams } from 'react-router-dom'
import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { Loading, ErrorState, EmptyState, BackLink } from '../components/ui'
import { TrendLines, VolumeTrend } from '../components/charts'

export default function Trends() {
  const { id } = useParams()
  const { data, error, loading, reload } = useFetch(() => api.trends(id), [id])

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />
  if (!data.available) return (
    <div><BackLink to={`/product/${id}`}>Back</BackLink><EmptyState message={data.note} /></div>
  )

  return (
    <div>
      <BackLink to={`/product/${id}`}>Back to analysis</BackLink>
      <h1 style={{ margin: '10px 0 16px' }}>Review trends</h1>
      <div className="card" style={{ marginBottom: 18 }}>
        <h3>Rating & positive sentiment over time</h3>
        <TrendLines points={data.points} />
      </div>
      <div className="card" style={{ marginBottom: 18 }}>
        <h3>Review volume</h3>
        <VolumeTrend points={data.points} />
      </div>
      {Object.keys(data.aspect_trends).length > 0 && (
        <div className="card">
          <h3>Aspect sentiment trend (most discussed)</h3>
          {Object.entries(data.aspect_trends).map(([asp, series]) => (
            <div key={asp} style={{ marginBottom: 10 }}>
              <strong style={{ textTransform: 'capitalize' }}>{asp}</strong>
              <div className="row" style={{ gap: 4 }}>
                {series.map((s) => (
                  <span key={s.month} className={`chip ${s.score >= 0.3 ? 'pos' : s.score <= -0.3 ? 'neg' : 'neu'}`} title={s.month}>
                    {s.month.slice(2)}: {s.score ?? '—'}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
