import { useEffect, useState } from 'react'
import { getHealth, getProducts } from './services/api'
import './App.css'

function App() {
  const [health, setHealth] = useState(null)
  const [products, setProducts] = useState([])
  const [error, setError] = useState(null)

  useEffect(() => {
    getHealth().then(setHealth).catch((e) => setError(e.message))
    getProducts().then(setProducts).catch((e) => setError(e.message))
  }, [])

  return (
    <main className="app">
      <h1>Product Review Analysis & Recommendation</h1>
      <p className="status">
        Backend:{' '}
        {error ? (
          <span className="bad">unreachable ({error})</span>
        ) : health ? (
          <span className="ok">
            {health.status} · MongoDB {health.mongodb ? 'connected' : 'offline'}
          </span>
        ) : (
          'checking…'
        )}
      </p>

      <h2>Products</h2>
      {products.length === 0 && !error ? (
        <p>Loading products…</p>
      ) : (
        <ul className="products">
          {products.map((p) => (
            <li key={p.product_id}>
              <strong>{p.name}</strong> — ${p.price} · ⭐ {p.rating}
              <span className="cat"> ({p.category})</span>
            </li>
          ))}
        </ul>
      )}
    </main>
  )
}

export default App
