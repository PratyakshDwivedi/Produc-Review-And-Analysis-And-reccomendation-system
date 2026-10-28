import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { useAuth } from '../context/AuthContext'
import { Loading, ErrorState, BackLink } from '../components/ui'
import { PriceLine } from '../components/charts'

export default function PriceTracking() {
  const { id } = useParams()
  const { user } = useAuth()
  const { data, error, loading, reload } = useFetch(() => api.priceHistory(id), [id])
  const [target, setTarget] = useState('')
  const [msg, setMsg] = useState(null)

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />

  async function createAlert() {
    if (!target) return
    try { await api.createAlert(id, Number(target)); setMsg('Alert created. Check Notifications.') }
    catch (e) { setMsg(e.message) }
  }

  return (
    <div>
      <BackLink to={`/product/${id}`}>Back to analysis</BackLink>
      <h1 style={{ margin: '10px 0 8px' }}>{data.name} · price tracking</h1>
      <p className="notice">{data.note}</p>
      <div className="grid cols-4" style={{ margin: '16px 0' }}>
        <div className="card"><div className="muted">Current</div><div className="price" style={{ fontSize: '1.5rem' }}>${data.current_price}</div></div>
        <div className="card"><div className="muted">Lowest</div><div style={{ fontSize: '1.5rem' }}>${data.min_price}</div></div>
        <div className="card"><div className="muted">Highest</div><div style={{ fontSize: '1.5rem' }}>${data.max_price}</div></div>
        <div className="card"><div className="muted">12-mo change</div><div style={{ fontSize: '1.5rem' }}>{data.change >= 0 ? '+' : ''}${data.change}</div></div>
      </div>
      <div className="card"><h3>Price history</h3><PriceLine history={data.history} /></div>

      <div className="card" style={{ marginTop: 18 }}>
        <h3>Price drop alert</h3>
        {user ? (
          <div className="row">
            <input type="number" placeholder="Notify me below $…" value={target} onChange={(e) => setTarget(e.target.value)} style={{ maxWidth: 220 }} />
            <button className="btn" onClick={createAlert}>Create alert</button>
            {msg && <span className="muted">{msg}</span>}
          </div>
        ) : <p className="muted">Please <Link to="/login">log in</Link> to create price alerts.</p>}
      </div>
    </div>
  )
}
