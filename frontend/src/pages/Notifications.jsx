import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import { Loading, ErrorState, EmptyState, PageHead } from '../components/ui'

export default function Notifications() {
  const { data, error, loading, reload } = useFetch(() => api.notifications(), [])

  async function read(id) { await api.readNotification(id); reload() }
  async function readAll() { await api.readAllNotifications(); reload() }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />

  return (
    <div>
      <div className="spread">
        <PageHead title="Notifications">{data.unread} unread</PageHead>
        {data.items.length > 0 && <button className="btn ghost sm" onClick={readAll}>Mark all read</button>}
      </div>
      {data.items.length === 0 ? <EmptyState message="No notifications yet." /> : (
        <div className="grid">
          {data.items.map((n) => (
            <div key={n.id} className="card" style={{ padding: 14, opacity: n.read ? 0.6 : 1 }}>
              <div className="spread">
                <span>{n.message}</span>
                {!n.read && <button className="btn ghost sm" onClick={() => read(n.id)}>Mark read</button>}
              </div>
              <div className="muted" style={{ fontSize: '0.78rem' }}>{n.kind} · {new Date(n.created_at).toLocaleString()}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
