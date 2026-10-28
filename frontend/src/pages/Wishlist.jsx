import { api } from '../services/api'
import { useFetch } from '../hooks/useFetch'
import ProductCard from '../components/ProductCard'
import { Loading, ErrorState, EmptyState, PageHead } from '../components/ui'

export default function Wishlist() {
  const { data, error, loading, reload } = useFetch(() => api.wishlist(), [])

  async function remove(id) { await api.removeWishlist(id); reload() }

  if (loading) return <Loading />
  if (error) return <ErrorState message={error} onRetry={reload} />

  return (
    <div>
      <PageHead title="Your wishlist">Saved products for quick access.</PageHead>
      {data.length === 0 ? <EmptyState message="Your wishlist is empty. Add products from their analysis page." />
        : (
          <div className="grid cols-4">
            {data.map((p) => (
              <ProductCard key={p.product_id} product={p}
                action={<button className="btn ghost sm" onClick={() => remove(p.product_id)}>Remove</button>} />
            ))}
          </div>
        )}
    </div>
  )
}
