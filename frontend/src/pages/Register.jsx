import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function Register() {
  const { register } = useAuth()
  const nav = useNavigate()
  const [form, setForm] = useState({ name: '', email: '', password: '' })
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(false)

  function set(k, v) { setForm((f) => ({ ...f, [k]: v })) }

  async function submit(e) {
    e.preventDefault(); setBusy(true); setError(null)
    try { await register(form.email, form.password, form.name); nav('/', { replace: true }) }
    catch (err) { setError(err.message) } finally { setBusy(false) }
  }

  return (
    <div style={{ maxWidth: 400, margin: '24px auto' }}>
      <h1>Create your account</h1>
      <form className="card" onSubmit={submit}>
        {error && <p className="chip neg" style={{ marginBottom: 12 }}>{error}</p>}
        <div className="field"><label>Name</label>
          <input value={form.name} onChange={(e) => set('name', e.target.value)} /></div>
        <div className="field"><label>Email</label>
          <input type="email" value={form.email} onChange={(e) => set('email', e.target.value)} required /></div>
        <div className="field"><label>Password (min 6 characters)</label>
          <input type="password" value={form.password} onChange={(e) => set('password', e.target.value)} required minLength={6} /></div>
        <button className="btn" style={{ width: '100%' }} disabled={busy}>{busy ? 'Creating…' : 'Sign up'}</button>
        <p className="muted" style={{ marginTop: 12, marginBottom: 0, fontSize: '0.85rem' }}>
          Already have an account? <Link to="/login">Sign in</Link>
        </p>
      </form>
    </div>
  )
}
