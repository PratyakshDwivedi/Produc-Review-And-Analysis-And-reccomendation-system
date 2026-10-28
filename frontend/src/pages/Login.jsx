import { useState } from 'react'
import { Link, useNavigate, useLocation } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Login() {
  const { login } = useAuth()
  const nav = useNavigate()
  const loc = useLocation()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  async function submit(e) {
    e.preventDefault(); setBusy(true); setError(null)
    try { await login(email, password); nav(loc.state?.from || '/', { replace: true }) }
    catch (err) { setError(err.message) } finally { setBusy(false) }
  }

  return (
    <div style={{ maxWidth: 400, margin: '24px auto' }}>
      <h1>Welcome back</h1>
      <form className="card" onSubmit={submit}>
        {error && <p className="chip neg" style={{ marginBottom: 12 }}>{error}</p>}
        <div className="field"><label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required /></div>
        <div className="field"><label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required /></div>
        <button className="btn" style={{ width: '100%' }} disabled={busy}>{busy ? 'Signing in…' : 'Sign in'}</button>
        <p className="muted" style={{ marginTop: 12, marginBottom: 0, fontSize: '0.85rem' }}>
          No account? <Link to="/register">Create one</Link>
        </p>
      </form>
    </div>
  )
}
