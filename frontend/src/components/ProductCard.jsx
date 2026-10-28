import { Link } from 'react-router-dom'
import { Stars, ProductThumb } from './ui'

export default function ProductCard({ product, action }) {
  return (
    <div className="card product-card">
      <ProductThumb name={product.name} />
      <div className="spread">
        <strong>{product.name}</strong>
        <span className="price">${product.price}</span>
      </div>
      <div className="meta">{product.brand} · {product.category}</div>
      <div className="row">
        <Stars value={product.rating} />
        <span className="muted" style={{ fontSize: '0.82rem' }}>
          {product.rating} ({product.review_count} reviews)
        </span>
      </div>
      <div className="row" style={{ marginTop: 8 }}>
        <Link className="btn sm" to={`/product/${product.product_id}`}>Analyze</Link>
        {action}
      </div>
    </div>
  )
}
