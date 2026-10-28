import { useEffect, useState } from 'react'
import { api } from '../services/api'
import { PageHead, Stars } from '../components/ui'

export default function RatingPredict() {
  const [text, setText] = useState('')
  const [result, setResult] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const [tf, setTf] = useState(null)

  useEffect(() => { api.transformerStatus().then(setTf).catch(() => {}) }, [])

  async function predict() {
    if (!text.trim()) return
    setBusy(true); setError(null)
    try { setResult(await api.predictRating(text)) } catch (e) { setError(e.message) } finally { setBusy(false) }
  }

  return (
    <div>
      <PageHead title="Rating prediction">
        Estimate a star rating from review text (TF-IDF + Ridge regression). This is an estimate and may
        differ from a customer's actual rating.
      </PageHead>
      <div className="card">
        <textarea rows={4} placeholder="Paste a review…" value={text} onChange={(e) => setText(e.target.value)} />
        <button className="btn" style={{ marginTop: 10 }} onClick={predict} disabled={busy}>
          {busy ? 'Predicting…' : 'Predict rating'}
        </button>
        {error && <p className="chip neg" style={{ marginTop: 10 }}>{error}</p>}
        {result && (
          <div style={{ marginTop: 16 }}>
            {result.predicted_rating != null ? (
              <div className="row"><span style={{ fontSize: '2rem' }}>{result.predicted_rating}</span><Stars value={result.predicted_rating} /></div>
            ) : <p className="muted">{result.note}</p>}
            <p className="muted" style={{ fontSize: '0.82rem' }}>{result.note}</p>
          </div>
        )}
      </div>
      <p className="notice" style={{ marginTop: 16 }}>
        Transformer (DistilBERT) sentiment: {tf?.available ? 'enabled and loaded' : 'disabled by default'}.
        {' '}Baseline TF-IDF model is always active. Enable the transformer with ENABLE_TRANSFORMER=1 (requires transformers + torch).
      </p>
    </div>
  )
}
