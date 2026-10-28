import { createContext, useContext, useEffect, useState } from 'react'
import { api, setToken } from '../services/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    let active = true
    const t = (() => { try { return localStorage.getItem('token') } catch { return null } })()
    if (!t) { setLoading(false); return }
    api.me().then((u) => active && setUser(u)).catch(() => setToken(null)).finally(() => active && setLoading(false))
    return () => { active = false }
  }, [])

  async function login(email, password) {
    const res = await api.login(email, password)
    setToken(res.token); setUser(res.user); return res.user
  }
  async function register(email, password, name) {
    const res = await api.register(email, password, name)
    setToken(res.token); setUser(res.user); return res.user
  }
  function logout() { setToken(null); setUser(null) }

  return (
    <AuthContext.Provider value={{ user, loading, login, register, logout, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

export const useAuth = () => useContext(AuthContext)
