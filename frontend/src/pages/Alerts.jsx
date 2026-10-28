import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { Loading, ErrorState, EmptyState, PageHead } from '../components/ui'

export default function Alerts() {
  const { data, error, loading, reload } = useFetch(() => api.alerts(), [])

  async function toggle(a) { await api.updateAlert(a.id, { active: !a.active }); reload() }
  async function remove(id) { await api.deleteAlert(id); reload() }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />

  return (
    <div>
      <PageHead title="Price alerts">
        Alerts are evaluated whenever you open Alerts or Notifications. Without an external scheduler they
        only run while you're active in the app.
      </PageHead>
      {data.length === 0 ? <EmptyState message="No alerts yet. Create one from a product's Price page." />
        : (
          <table className="compare">
            <thead><tr><th>Product</th><th>Target</th><th>Status</th><th>Triggered</th><th></th></tr></thead>
            <tbody>
              {data.map((a) => (
                <tr key={a.id}>
                  <td className="rowhead">{a.product_id}</td>
                  <td>${Math.round(a.target_price)}</td>
                  <td><span className={`chip ${a.active ? 'pos' : 'neu'}`}>{a.active ? 'active' : 'paused'}</span></td>
                  <td>{a.triggered ? 'yes' : 'no'}</td>
                  <td>
                    <button className="btn ghost sm" onClick={() => toggle(a)}>{a.active ? 'Pause' : 'Resume'}</button>{' '}
                    <button className="btn ghost sm" onClick={() => remove(a.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
    </div>
  )
}
