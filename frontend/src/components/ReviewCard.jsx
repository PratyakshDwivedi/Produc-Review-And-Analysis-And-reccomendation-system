import { Stars, SentimentChip } from './ui'

export default function ReviewCard({ review }) {
  const aspects = review.aspects || {}
  return (
    <div className="card" style={{ padding: 14 }}>
      <div className="spread">
        <Stars value={review.rating} />
        <span className="muted" style={{ fontSize: '0.8rem' }}>{review.date}</span>
      </div>
      <p style={{ margin: '8px 0' }}>{review.review_text}</p>
      <div className="row">
        {review.sentiment && <SentimentChip value={review.sentiment} />}
        {Object.entries(aspects).map(([a, s]) => (
          <span key={a} className={`chip ${s === 'positive' ? 'pos' : s === 'negative' ? 'neg' : 'neu'}`}>
            {a}: {s}
          </span>
        ))}
      </div>
    </div>
  )
}
