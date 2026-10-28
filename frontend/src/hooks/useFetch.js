import { useEffect, useState, useCallback } from 'react'

// Generic data loader. `fn` should be a stable function returning a promise.
export function useFetch(fn, deps = []) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const run = useCallback(() => {
    setLoading(true); setError(null)
    return fn()
      .then(setData)
      .catch((e) => setError(e.message || 'Something went wrong'))
      .finally(() => setLoading(false))
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps)

  useEffect(() => { let active = true; run(); return () => { active = false } }, [run])

  return { data, error, loading, reload: run }
}
