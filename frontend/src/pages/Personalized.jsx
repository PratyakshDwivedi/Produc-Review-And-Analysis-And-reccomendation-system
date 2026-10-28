import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { api } from '../services/api'
import { Loading, ErrorState, PageHead, Stars } from '../components/ui'
import { ASPECTS } from '../constants'

export default function Personalized() {
  const [prefs, setPrefs] = useState(null)
  const [categories, setCategories] = useState([])
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  async function load() {
    setLoading(true); setError(null)
    try {
      const [p, d, c] = await Promise.all([api.getPreferences(), api.personalized(), api.categories()])
      setPrefs(p); setData(d); setCategories(c)
    } catch (e) { setError(e.message) } finally { setLoading(false) }
  }
  useEffect(() => { load() }, [])

  function toggleAspect(a) {
    setPrefs((p) => ({ ...p, preferred_aspects: p.preferred_aspects.includes(a)
      ? p.preferred_aspects.filter((x) => x !== a) : [...p.preferred_aspects, a] }))
  }

  async function save() {
    setSaving(true)
    try {
      await api.setPreferences({
        category: prefs.category || null, budget: prefs.budget ? Number(prefs.budget) : null,
        preferred_aspects: prefs.preferred_aspects, min_rating: Number(prefs.min_rating) || 0,
      })
      setData(await api.personalized())
    } catch (e) { setError(e.message) } finally { setSaving(false) }
  }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={load} />

  return (
    <div>
      <PageHead title="Personalized recommendations">Set your preferences; recommendations update to match.</PageHead>
      <div className="grid cols-2">
        <div className="card">
          <h3>Your preferences</h3>
          <div className="field"><label>Category</label>
            <select value={prefs.category || ''} onChange={(e) => setPrefs({ ...prefs, category: e.target.value })}>
              <option value="">Any</option>{categories.map((c) => <option key={c} value={c}>{c}</option>)}
            </select>
          </div>
          <div className="field"><label>Max budget ($)</label>
            <input type="number" value={prefs.budget || ''} onChange={(e) => setPrefs({ ...prefs, budget: e.target.value })} />
          </div>
          <div className="field"><label>Preferred aspects</label>
            <div className="tag-list">
              {ASPECTS.map((a) => (
                <button key={a} onClick={() => toggleAspect(a)} style={{ cursor: 'pointer', border: 0 }}
                  className={`chip ${prefs.preferred_aspects.includes(a) ? 'pos' : ''}`}>{a}</button>
              ))}
            </div>
          </div>
          <button className="btn" onClick={save} disabled={saving}>{saving ? 'Saving…' : 'Save & refresh'}</button>
        </div>

        <div className="card">
          <h3>For you</h3>
          <p className="muted" style={{ fontSize: '0.85rem' }}>{data.methodology}</p>
          {data.ranking.slice(0, 8).map((r) => (
            <div key={r.product_id} className="spread" style={{ padding: '8px 0', borderBottom: '1px solid var(--border)' }}>
              <Link to={`/product/${r.product_id}`}>{r.name}</Link>
              <span><Stars value={r.rating} /> <span className="chip pos">{r.rank_score}</span></span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
