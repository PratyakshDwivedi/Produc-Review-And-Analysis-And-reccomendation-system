import { Link } from 'react-router-dom'
import { Search, BarChart3, Sparkles, Scale } from 'lucide-react'
import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import ProductCard from '../components/ProductCard'
import { Loading, ErrorState } from '../components/ui'

const FEATURES = [
  [Search, 'Search & overview', 'Find products and see sentiment at a glance.'],
  [BarChart3, 'Aspect analysis', 'Camera, battery, display and more — scored from real reviews.'],
  [Sparkles, 'Explainable recommendations', 'Natural-language queries with transparent reasons.'],
  [Scale, 'Compare & rank', 'Side-by-side comparison and confidence-adjusted rankings.'],
]

export default function Home() {
  const { data, error, loading, reload } = useFetch(() => api.products(), [])
  return (
    <div>
      <section className="hero">
        <h1>Understand thousands of reviews in seconds.</h1>
        <p>ReviewLeaf analyzes product reviews for sentiment, aspects, strengths and
          weaknesses, then turns them into clear, explainable recommendations.</p>
        <div className="row" style={{ marginTop: 16 }}>
          <Link className="btn" to="/search">Explore products</Link>
          <Link className="btn ghost" to="/recommend">Get a recommendation</Link>
        </div>
      </section>

      <section className="grid cols-4" style={{ margin: '28px 0' }}>
        {FEATURES.map(([Icon, title, desc]) => (
          <div className="card" key={title}>
            <Icon size={20} color="var(--primary)" />
            <h3 style={{ marginTop: 10 }}>{title}</h3>
            <p className="muted" style={{ margin: 0, fontSize: '0.9rem' }}>{desc}</p>
          </div>
        ))}
      </section>

      <section>
        <div className="spread"><h2>Featured products</h2><Link to="/search">View all →</Link></div>
        {loading ? <Loading /> : error ? <ErrorState message={error} onRetry={reload} /> : (
          <div className="grid cols-4" style={{ marginTop: 12 }}>
            {data.slice(0, 8).map((p) => <ProductCard key={p.product_id} product={p} />)}
          </div>
        )}
      </section>
    </div>
  )
}
