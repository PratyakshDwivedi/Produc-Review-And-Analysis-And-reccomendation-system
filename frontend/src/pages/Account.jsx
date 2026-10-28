import { useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { PageHead } from '../components/ui'

export default function Account() {
  const { user, setUser, logout } = useAuth()
  const [name, setName] = useState(user?.name || '')
  const [msg, setMsg] = useState(null)
  const [busy, setBusy] = useState(false)

  async function save() {
    setBusy(true); setMsg(null)
    try { const u = await api.updateAccount(name); setUser(u); setMsg('Saved.') }
    catch (e) { setMsg(e.message) } finally { setBusy(false) }
  }

  return (
    <div style={{ maxWidth: 560 }}>
      <PageHead title="Account settings" />
      <div className="card">
        <div className="field"><label>Email</label><input value={user.email} disabled /></div>
        <div className="field"><label>Name</label><input value={name} onChange={(e) => setName(e.target.value)} /></div>
        <div className="row">
          <button className="btn" onClick={save} disabled={busy}>{busy ? 'Saving…' : 'Save changes'}</button>
          {msg && <span className="muted">{msg}</span>}
        </div>
      </div>
      <div className="card" style={{ marginTop: 18 }}>
        <h3>Shortcuts</h3>
        <div className="row">
          <Link className="btn ghost sm" to="/personalized">Preferences & recommendations</Link>
          <Link className="btn ghost sm" to="/wishlist">Wishlist</Link>
          <Link className="btn ghost sm" to="/alerts">Alerts</Link>
          <button className="btn ghost sm" onClick={logout}>Log out</button>
        </div>
      </div>
    </div>
  )
}
