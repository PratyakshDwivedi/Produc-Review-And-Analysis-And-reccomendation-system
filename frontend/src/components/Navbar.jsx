import { useEffect, useState } from 'react'
import { NavLink, useNavigate } from 'react-router-dom'
import { Bell, Leaf } from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { api } from '../services/api'

const LINKS = [
  ['/', 'Home'], ['/search', 'Search'], ['/recommend', 'Recommend'],
  ['/compare', 'Compare'], ['/rankings', 'Rankings'],
  ['/rating-predict', 'Rating'], ['/assistant', 'Assistant'],
]

export default function Navbar() {
  const { user, logout } = useAuth()
  const nav = useNavigate()
  const [unread, setUnread] = useState(0)

  useEffect(() => {
    if (!user) { setUnread(0); return }
    api.notifications().then((n) => setUnread(n.unread || 0)).catch(() => {})
  }, [user])

  return (
    <header className="nav">
      <div className="container nav-inner">
        <NavLink to="/" className="brand">
          <span className="dot"><Leaf size={14} /></span> ReviewLeaf
        </NavLink>
        <nav className="nav-links">
          {LINKS.map(([to, label]) => (
            <NavLink key={to} to={to} end={to === '/'}>{label}</NavLink>
          ))}
          {user && <NavLink to="/personalized">For you</NavLink>}
          {user && <NavLink to="/wishlist">Wishlist</NavLink>}
          {user && <NavLink to="/alerts">Alerts</NavLink>}
        </nav>
        <div className="nav-right">
          {user && (
            <NavLink to="/notifications" className="btn ghost sm" title="Notifications">
              <Bell size={15} />{unread > 0 ? ` ${unread}` : ''}
            </NavLink>
          )}
          {user ? (
            <>
              <NavLink to="/account" className="muted" style={{ fontSize: '0.85rem' }}>{user.name || user.email}</NavLink>
              <button className="btn ghost sm" onClick={() => { logout(); nav('/') }}>Logout</button>
            </>
          ) : (
            <>
              <NavLink to="/login" className="btn ghost sm">Login</NavLink>
              <NavLink to="/register" className="btn sm">Sign up</NavLink>
            </>
          )}
        </div>
      </div>
    </header>
  )
}
