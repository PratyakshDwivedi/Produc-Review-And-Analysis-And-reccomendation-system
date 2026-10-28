import { Link } from 'react-router-dom'

export function Loading({ label = 'Loading…' }) {
  return <div className="state"><div className="spinner" />{label}</div>
}

export function ErrorState({ message, onRetry }) {
  return (
    <div className="state">
      <p>⚠ {message || 'Failed to load.'}</p>
      {onRetry && <button className="btn ghost sm" onClick={onRetry}>Retry</button>}
    </div>
  )
}

export function EmptyState({ message = 'Nothing here yet.', children }) {
  return <div className="state"><p>{message}</p>{children}</div>
}

export function Stars({ value = 0 }) {
  const full = Math.round(value)
  return <span className="stars" title={`${value} / 5`}>{'★'.repeat(full)}{'☆'.repeat(5 - full)}</span>
}

export function SentimentChip({ value }) {
  const cls = value === 'positive' ? 'pos' : value === 'negative' ? 'neg' : 'neu'
  return <span className={`chip ${cls}`}>{value}</span>
}

export function ScoreChip({ score }) {
  const v = score >= 0.3 ? 'pos' : score <= -0.3 ? 'neg' : 'neu'
  return <span className={`chip ${v}`}>{score > 0 ? '+' : ''}{score}</span>
}

export function Bar({ value, max = 1 }) {
  const pct = Math.max(0, Math.min(100, (value / max) * 100))
  return <div className="bar"><span style={{ width: `${pct}%` }} /></div>
}

export function ProductThumb({ name }) {
  return <div className="thumb">{(name || '?').charAt(0)}</div>
}

export function PageHead({ title, children }) {
  return <div className="page-head"><h1>{title}</h1>{children && <p>{children}</p>}</div>
}

export function BackLink({ to, children }) {
  return <Link to={to} className="muted" style={{ fontSize: '0.85rem' }}>← {children}</Link>
}
